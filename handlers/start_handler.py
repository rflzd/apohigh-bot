from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.base import SessionLocal
from db.models.user import User

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name

    # İstifadəçi bazada yoxlanır və varsa, məlumatları alırıq
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        # İstifadəçi bazada tapılmadıqda, onu əlavə edirik
        user = User(telegram_id=user_id, full_name=full_name)
        session.add(user)
        session.commit()

    # İstifadəçiyə seçimlər göndəririk, abunəlik yoxlaması olmadan
    keyboard = [
        ["⚽ Canlı", "📅 Prematch"],
        ["Sevimli komandalar 💖", "Kupon analizi 🎯", "AI analiz"]
    ]
    
    # İstifadəçiyə seçimlər təqdim edirik
    await update.message.reply_text(
        "Xoş gəlmisiniz Apohigh botuna! \nZəhmət olmasa bir seçim edin:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    session.close()  # Sessiyanı bağlayırıq
