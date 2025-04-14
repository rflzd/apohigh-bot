from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.config import M10_ACCOUNT, CARD_NUMBER


async def payment_method_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pay_m10":
        text = (
            f"💰 *M10 ilə ödəniş üçün:*\n"
            f"➡️ Hesab nömrəsi: `{M10_ACCOUNT}`\n\n"
            "📤 Zəhmət olmasa ödənişi etdikdən sonra çeki yükləyin."
        )
        copy_button = InlineKeyboardButton("📋 Kopyala M10 Hesabı", switch_inline_query_current_chat=M10_ACCOUNT)

    elif query.data == "pay_card2card":
        text = (
            f"💳 *Kartla ödəniş üçün:*\n"
            f"➡️ Kart nömrəsi: `{CARD_NUMBER}`\n\n"
            "📤 Zəhmət olmasa ödənişi etdikdən sonra çeki yükləyin."
        )
        copy_button = InlineKeyboardButton("📋 Kopyala Kart Nömrəsi", switch_inline_query_current_chat=CARD_NUMBER)

    else:
        text = "Seçim tapılmadı."
        copy_button = None

    keyboard = InlineKeyboardMarkup([[copy_button]]) if copy_button else None

    await query.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
