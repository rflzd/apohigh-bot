from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
import json

async def add_favorite_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user or not user.is_subscribed:
        await update.message.reply_text("🔒 Bu xüsusiyyət yalnız abunəliklə aktivdir.")
        session.close()
        return

    if not context.args:
        await update.message.reply_text("Zəhmət olmasa komanda adını yazın. Misal: `/addfav Barcelona`")
        session.close()
        return

    team_to_add = " ".join(context.args)

    try:
        teams = json.loads(user.favorite_teams or "[]")
    except:
        teams = []

    if team_to_add in teams:
        await update.message.reply_text(f"{team_to_add} artıq sevimlilərinizdə var.")
    else:
        teams.append(team_to_add)
        user.favorite_teams = json.dumps(teams)
        session.commit()
        await update.message.reply_text(f"{team_to_add} sevimlilərə əlavə olundu ✅")

    session.close()
