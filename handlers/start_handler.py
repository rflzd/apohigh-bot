from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ApplicationBuilder, ContextTypes
from db.base import SessionLocal
from db.models.user import User

# Start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name

    # İstifadəçinin məlumatlarını yoxlayaq və əlavə edək
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        user = User(telegram_id=user_id, full_name=full_name)
        session.add(user)
        session.commit()

    # Abunəlik statusunu yoxlayaq
    if user.is_subscribed == 0:
        # Abunə olmayan istifadəçilərə yalnız canlı və prematch seçimlərini göstəririk
        keyboard = [
            [InlineKeyboardButton("⚽ Canlı", callback_data="live_matches"),
             InlineKeyboardButton("📅 Prematch", callback_data="prematch")]
        ]
    else:
        # Abunə olan istifadəçilərə daha çox seçim göstəririk
        keyboard = [
            [InlineKeyboardButton("⚽ Canlı", callback_data="live_matches"),
             InlineKeyboardButton("📅 Prematch", callback_data="prematch")],
            [InlineKeyboardButton("Sevimli komandalar 💖", callback_data="favorite_teams"),
             InlineKeyboardButton("Kupon analizi 🎯", callback_data="coupon_analysis"),
             InlineKeyboardButton("AI analiz", callback_data="ai_analysis")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    # İstifadəçiyə mesaj göndəririk
    await update.message.reply_text(
        "Xoş gəlmisiniz! Zəhmət olmasa seçim edin:",
        reply_markup=reply_markup
    )

    session.close()  # Sessiyanı bağlayırıq

# Callback funksiyası, istifadəçi düymələrə basdıqda cavab verir
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Callback data ilə seçimi alırıq
    if query.data == "favorite_teams":
        await query.edit_message_text(text="Sevimli komandalar seçildi!")
    elif query.data == "coupon_analysis":
        await query.edit_message_text(text="Kupon analizi seçildi!")
    elif query.data == "live_matches":
        await query.edit_message_text(text="Canlı matçlar seçildi!")
    elif query.data == "prematch":
        await query.edit_message_text(text="Prematch seçildi!")
    elif query.data == "ai_analysis":
        await query.edit_message_text(text="AI analiz seçildi!")

# Botu qururuq
async def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Handler-ları əlavə edirik
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Botu işə salırıq
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
