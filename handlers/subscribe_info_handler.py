from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def subscribe_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 *Apohigh Premium Abunəliyi ilə əldə edəcəksiniz:*\n\n"
        "✅ AI əsaslı mərc təhlilləri\n"
        "✅ Sevimli komandalar sistemi\n"
        "✅ Mərc kuponu analizi\n"
        "✅ Reklamsız və sürətli cavablar\n\n"
        "*Abunəlik haqqı:* {SUBSCRIPTION_PRICE}\n\n"
        "Ödəniş metodunu seçin:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 M10 ilə ödə", callback_data="pay_m10")],
        [InlineKeyboardButton("💳 Card2Card ilə ödə", callback_data="pay_card2card")]
    ])

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
