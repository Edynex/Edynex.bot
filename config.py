import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))
PIX_KEY = "32984030156"

PLANS = {
    "free": {"price": 0, "videos": 1},
    "weekly": {"price": 19.90, "videos": 3},
    "monthly": {"price": 49.90, "videos": 12},
    "annual": {"price": 297.00, "videos": 160},
}
