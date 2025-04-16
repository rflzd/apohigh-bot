from telegram import Update
from telegram.ext import ContextTypes
from db.base import SessionLocal
from db.models.user import User

async def forward_to_admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not query.data.startswith("forward_admin_"):
        return

    try:
        telegram_id = int(query.data.split("_")[-1])
    except ValueError:
        await query.message.reply_text("❌ Telegram ID düzgün formatda deyil.")
        return

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if not user:
        await query.message.reply_text("❌ İstifadəçi tapılmadı.")
        session.close()
        return

    user.is_subscribed = True
    session.commit()
    session.close()

    try:
        await context.bot.send_message(
            chat_id=telegram_id,
            text="🎉 Abunəliyiniz təsdiqləndi! Artıq premium funksiyalara girişiniz var."
        )
        await query.message.reply_text("✅ İstifadəçi uğurla premium edildi.")
    except Exception as e:
        print(f"İstifadəçiyə mesaj göndərilərkən xəta: {e}")
