from telegram import Update
from telegram.ext import ContextTypes
from db.base import SessionLocal
from db.models.user import User

async def favorites_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id

    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if not user or not user.favorite_teams:
        await update.message.reply_text("Sevimli komandalar siyahınız boşdur.")
        return

    teams = user.favorite_teams.split(",")
    msg = "💖 Sevimli komandalarınız:\n\n"
    for team in teams:
        msg += f"• {team.strip()}\n"

    await update.message.reply_text(msg)
