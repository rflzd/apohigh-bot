from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User

async def payment_upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        await update.message.reply_text("Zəhmət olmasa əvvəl /start yazın.")
        session.close()
        return

    if update.message.photo:
        photo = update.message.photo[-1]
        file_id = photo.file_id

        user.payment_proof_url = file_id
        session.commit()

        await update.message.reply_text(
            "✅ Təşəkkürlər! Ödəniş çeki uğurla qəbul edildi. Admin yoxladıqdan sonra abunəliyiniz aktiv ediləcək."
        )
    else:
        await update.message.reply_text("📷 Zəhmət olmasa bir şəkil yükləyin.")

    session.close()
