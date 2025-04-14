from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
import json

async def favorites_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user or not user.is_subscribed:
        await update.message.reply_text("🔒 Bu xüsusiyyət yalnız abunəliklə aktivdir.")
        session.close()
        return

    # Sevimli komandaları oxu
    try:
        teams = json.loads(user.favorite_teams or "[]")
    except:
        teams = []

    if not teams:
        await update.message.reply_text("Sizin sevimli komandanız yoxdur. Əlavə etmək üçün `/addfav` yazın.")
    else:
        keyboard = [[team] for team in teams]
        await update.message.reply_text(
            "Sevimli komandalarınızdan birini seçin:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    session.close()
