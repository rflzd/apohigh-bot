from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from db.models.moderator import Moderator
from utils.config import ADMIN_IDS

async def pending_payments_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = SessionLocal()

    # Moderator və ya admin olduğunu yoxla
    is_admin = user_id in ADMIN_IDS
    is_moderator = session.query(Moderator).filter_by(telegram_id=user_id).first() is not None

    if not (is_admin or is_moderator):
        await update.message.reply_text("❌ Bu əmri yalnız admin və ya moderatorlar istifadə edə bilər.")
        session.close()
        return

    pending_users = session.query(User).filter(User.payment_proof_url != None, User.is_subscribed == False).all()
    
    if not pending_users:
        await update.message.reply_text("✅ Gözləmədə olan heç bir ödəniş yoxdur.")
        session.close()
        return

    for user in pending_users:
        caption = f"🧾 İstifadəçi: {user.full_name or 'Naməlum'}\nTelegram ID: `{user.telegram_id}`"

        if is_admin:
            caption += f"\n✅ Təsdiqlə: `/approve {user.telegram_id}`"
            await update.message.reply_photo(photo=user.payment_proof_url, caption=caption, parse_mode="Markdown")
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 Adminə göndər", callback_data=f"forward_admin_{user.telegram_id}")]
            ])
            await update.message.reply_photo(
                photo=user.payment_proof_url,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=keyboard
            )

    session.close()
