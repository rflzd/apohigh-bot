from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User

async def add_favorite_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id
    text = update.message.text.strip()

    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        await update.message.reply_text("❌ İstifadəçi tapılmadı. Zəhmət olmasa /start yazın.")
        session.close()
        return

    if not text:
        await update.message.reply_text("❗ Komanda adı boş ola bilməz.")
        session.close()
        return

    if user.favorite_teams:
        teams = user.favorite_teams.split(",")
        if text in teams:
            await update.message.reply_text("⚠️ Bu komanda artıq sevimlilərinizdə var.")
            session.close()
            return
        teams.append(text)
        user.favorite_teams = ",".join(teams)
    else:
        user.favorite_teams = text

    session.commit()
    session.close()

    await update.message.reply_text(f"✅ {text} sevimli komandalarınıza əlavə olundu!")
