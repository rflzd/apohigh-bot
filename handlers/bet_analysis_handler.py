from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from ai_analysis.recommendation import analyze_bet_coupon

async def bet_analysis_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if not user or not user.is_subscribed:
        await update.message.reply_text("🔒 Kupon analizi yalnız abunə olan istifadəçilər üçündür.")
        return

    if not message:
        await update.message.reply_text("Zəhmət olmasa kupon mətnini göndərin.")
        return

    analysis = analyze_bet_coupon(message)
    await update.message.reply_text(f"🤖 Kupon analizi nəticəsi:\n\n{analysis}", parse_mode="Markdown")
