from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from config import ADMIN_IDS

async def payment_upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_url = file.file_path

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        user = User(telegram_id=user_id, full_name=full_name)

    user.payment_proof_url = file_url
    session.add(user)
    session.commit()
    session.close()

    await update.message.reply_text("📤 Ödəniş çekiniz qeydə alındı. Qısa zamanda yoxlanılacaq ✅")

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=file_url,
                caption=(
                    f"💳 Yeni ödəniş çeki göndərildi!\n\n"
                    f"👤 {full_name}\n"
                    f"🆔 Telegram ID: `{user_id}`\n\n"
                    f"Təsdiqləmək üçün ↓\n"
                ),
                parse_mode="Markdown",
                reply_markup=None
            )
        except Exception as e:
            print(f"Admin mesajı göndərilərkən xəta: {e}")
