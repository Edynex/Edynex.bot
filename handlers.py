import nest_asyncio
nest_asyncio.apply()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from config import TOKEN, ADMIN_GROUP_ID, PIX_KEY, PLANS
from database import get_user, save_user
from editor import edit_style_by_niche

import asyncio

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_data = get_user(user.id)

    if not user_data:
        save_user(user.id, {"plan": "free", "videos_used": 0, "paid": False})

    keyboard = [
        [InlineKeyboardButton("🎁 Quero vídeo grátis", callback_data="free_video")],
        [InlineKeyboardButton("📦 Ver planos", callback_data="show_plans")],
        [InlineKeyboardButton("📞 Suporte", url=f"https://wa.me/{PIX_KEY}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Olá {user.first_name}! Bem-vindo ao Edynex.\n\n"
        "Quer um vídeo grátis para testar nossa edição? Ou deseja conhecer nossos planos?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_data = get_user(user.id) or {}

    if query.data == "free_video":
        if user_data.get("videos_used", 0) >= 1 and user_data.get("plan") == "free":
            await query.edit_message_text("Você já usou seu vídeo grátis. Que tal conhecer nossos planos?")
            return

        edited_video_path = edit_style_by_niche("default", "video_teste.mp4")
        user_data["videos_used"] = user_data.get("videos_used", 0) + 1
        save_user(user.id, user_data)

        await query.edit_message_text("Aqui está seu vídeo grátis! (Simulado) 🎬\n\nDepois conheça nossos planos para continuar.")

    elif query.data == "show_plans":
        keyboard = []
        for plan, info in PLANS.items():
            if plan == "free":
                continue
            price = info["price"]
            keyboard.append([InlineKeyboardButton(f"{plan.capitalize()} - R$ {price}", callback_data=f"plan_{plan}")])

        keyboard.append([InlineKeyboardButton("Voltar", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Escolha um plano:", reply_markup=reply_markup)

    elif query.data.startswith("plan_"):
        plan_selected = query.data.split("_")[1]
        price = PLANS[plan_selected]["price"]
        msg = (
            f"Você escolheu o plano {plan_selected.capitalize()} por R$ {price}.\n"
            f"Faça o pagamento via Pix na chave:\n{PIX_KEY}\n"
            "Depois envie o comprovante no grupo privado para ativação.\n\n"
            "Assim que confirmado, seu plano será ativado!"
        )
        await query.edit_message_text(msg)

    elif query.data == "start":
        await start(update, context)

async def handle_video(update: Update, context: CallbackContext):
    await update.message.reply_text("Recebi seu vídeo! Vamos processar e enviar a edição.")

    edited_path = edit_style_by_niche("default", "user_video.mp4")
    await update.message.reply_text(f"Seu vídeo editado está pronto: {edited_path}")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
