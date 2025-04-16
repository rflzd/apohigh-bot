from telegram import Update
from telegram.ext import ContextTypes
from db.base import SessionLocal
from db.models.user import User
from datetime import datetime, timedelta
from .admin_check import admin_check  # Admin yoxlama funksiyasını əlavə et

async def approve_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return  # Əgər admin yoxdursa, funksiyanı icra etmirik

    if not context.args:
        await update.message.reply_text("🛑 Zəhmət olmasa istifadəçi ID-sini yazın. Misal: /approve 123456789")
        return

    try:
        telegram_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("🚫 Telegram ID yalnız rəqəm olmalıdır.")
        return

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if not user:
        await update.message.reply_text("❌ Belə istifadəçi tapılmadı.")
        session.close()
        return

    if user.is_subscribed:
        await update.message.reply_text("ℹ️ Bu istifadəçi artıq abunədir.")
        session.close()
        return

    # ✅ Abunəliyi aktiv et və tarixləri təyin et
    user.is_subscribed = True
    user.subscription_start = datetime.utcnow()
    user.subscription_end = datetime.utcnow() + timedelta(days=30)
    session.commit()
    session.close()

    await update.message.reply_text(f"✅ {user.full_name or telegram_id} abunə kimi təsdiqləndi.")
