from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ApplicationBuilder, ContextTypes

# Start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inline keyboard yaratmaq
    keyboard = [
        [InlineKeyboardButton("Sevimli komandalar 💖", callback_data="favorite_teams"),
         InlineKeyboardButton("Kupon analizi 🎯", callback_data="coupon_analysis")],
        [InlineKeyboardButton("Canlı matçlar ⚽", callback_data="live_matches"),
         InlineKeyboardButton("Prematch ⚽", callback_data="prematch")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # İstifadəçiyə mesaj göndəririk
    await update.message.reply_text(
        "Xoş gəlmisiniz! Zəhmət olmasa seçim edin:",
        reply_markup=reply_markup
    )

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
