import os
import asyncio
from telegram.ext import Application, CommandHandler
from fastapi import FastAPI
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Bot rodando!")

bot_app.add_handler(CommandHandler("start", start))

web = FastAPI()

@web.get("/")
def root():
    return {"status": "ok", "bot": "running"}

async def main():
    asyncio.create_task(bot_app.run_polling())
    port = int(os.environ.get("PORT", 10000))
    config = uvicorn.Config(web, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
