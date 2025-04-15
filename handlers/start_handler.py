from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.user import User

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name

    # Check if the user exists in the database
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        user = User(telegram_id=user_id, full_name=full_name)
        session.add(user)
        session.commit()

    # Check user's subscription status
    if user.is_subscribed == 0:
        # Show only live and prematch options to unsubscribed users
        keyboard = [["⚽ Canlı", "📅 Prematch"]]
        await update.message.reply_text(
            "Xoş gəlmisiniz Apohigh botuna! \nZəhmət olmasa bir seçim edin:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        # Show live, prematch, and subscription features to subscribed users
        keyboard = [["⚽ Canlı", "📅 Prematch"], ["Sevimli komandalar 💖", "Kupon analizi 🎯", "AI analiz"]]
        await update.message.reply_text(
            "Xoş gəlmisiniz Apohigh botuna! \nZəhmət olmasa bir seçim edin:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    
    session.close()  # Close the session
