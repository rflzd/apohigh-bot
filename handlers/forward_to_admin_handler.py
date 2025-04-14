from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User
from utils.config import config

async def forward_to_admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        telegram_id = int(query.data.split("_")[-1])
    except:
        await query.message.reply_text("⚠️ ID formatı xətalıdır.")
        return

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    session.close()

    if not user:
        await query.message.reply_text("İstifadəçi tapılmadı.")
        return

    caption = (
        f"📤 Moderator tərəfindən yönləndirildi:\n"
        f"👤 {user.full_name or 'Naməlum'}\n"
        f"🆔 Telegram ID: `{user.telegram_id}`\n"
        f"✅ Təsdiqlə: `/approve {user.telegram_id}`"
    )

    for admin_id in ADMIN_IDS:
        await context.bot.send_photo(
            chat_id=admin_id,
            photo=user.payment_proof_url,
            caption=caption,
            parse_mode="Markdown"
        )

    await query.message.reply_text("✅ Şəkil adminə göndərildi.")
