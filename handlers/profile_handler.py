from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from datetime import datetime

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if not user:
        await update.message.reply_text("❌ İstifadəçi məlumatınız tapılmadı. Zəhmət olmasa /start yazın.")
        return

    status = "✅ *Aktiv abunəliyiniz var*" if user.is_subscribed else "🔓 *Abunəliyiniz yoxdur*"
    msg = (
        f"👤 *Ad:* {user.full_name or 'Naməlum'}\n"
        f"🆔 *Telegram ID:* `{user.telegram_id}`\n"
        f"{status}"
    )

    if user.is_subscribed:
        start = user.subscription_start.strftime('%Y-%m-%d') if user.subscription_start else "Naməlum"
        end = user.subscription_end.strftime('%Y-%m-%d') if user.subscription_end else "Naməlum"
        msg += f"\n📅 Başlanğıc: `{start}`\n⏳ Bitmə: `{end}`"

    if user.payment_proof_url:
        await update.message.reply_photo(
            photo=user.payment_proof_url,
            caption=msg,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(msg, parse_mode="Markdown")
