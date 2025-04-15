from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from .admin_check import admin_check  # Admin yoxlama funksiyasını əlavə et

async def pending_payments_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return  # Admin yoxdursa, funksiyanı icra etmirik

    session = SessionLocal()
    pending_users = session.query(User).filter(
        User.is_subscribed == False,
        User.payment_proof_url != None
    ).all()
    session.close()

    if not pending_users:
        await update.message.reply_text("📭 Hal-hazırda gözləyən ödəniş yoxdur.")
        return

    for user in pending_users:
        msg = (
            f"📌 Ödəniş gözləyir:\n\n"
            f"👤 Ad: {user.full_name}\n"
            f"🆔 Telegram ID: `{user.telegram_id}`\n"
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"forward_admin_{user.telegram_id}")]])
        try:
            await update.message.reply_photo(
                photo=user.payment_proof_url,
                caption=msg,
                parse_mode="Markdown",
                reply_markup=buttons
            )
        except Exception as e:
            print(f"Xəta: {e}")
