from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User

async def bet_analysis_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = SessionLocal()

    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if not user or not user.is_subscribed:
        await update.message.reply_text("🔒 Bu funksiyadan istifadə etmək üçün abunə olun.")
        return

    await update.message.reply_text(
        "🎯 Kupon analiz funksiyası aktivdir.\nZəhmət olmasa analiz etmək istədiyiniz kuponun şəklini göndərin."
    )
