import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")

M10_ACCOUNT = os.getenv("M10_ACCOUNT")
CARD_NUMBER = os.getenv("CARD_NUMBER")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

SUBSCRIPTION_PRICE = os.getenv("SUBSCRIPTION_PRICE", "3 AZN")

__all__ = [
    "BOT_TOKEN",
    "API_KEY",
    "API_BASE_URL",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_NAME",
    "DATABASE_URL",
    "ADMIN_IDS",
    "SUBSCRIPTION_PRICE",
    "M10_ACCOUNT",
    "CARD_NUMBER",
]
