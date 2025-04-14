from telegram import Update
from telegram.ext import ContextTypes
from config import M10_ACCOUNT, CARD_NUMBER, SUBSCRIPTION_PRICE

async def payment_method_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pay_m10":
        text = (
            f"💰 *M10 ilə ödəniş üçün:*\n"
            f"➡️ M10 Hesab: `{M10_ACCOUNT}`\n"
            f"💳 Məbləğ: *{SUBSCRIPTION_PRICE}*\n\n"
            f"📤 Zəhmət olmasa ödənişi etdikdən sonra çeki yükləyin.\n"
            f"Ödəniş yoxlanıldıqdan sonra abunəliyiniz aktiv ediləcək ✅"
        )
    elif query.data == "pay_card2card":
        text = (
            f"💳 *Kartla ödəniş üçün:*\n"
            f"➡️ Kart nömrəsi: `{CARD_NUMBER}`\n"
            f"💳 Məbləğ: *{SUBSCRIPTION_PRICE}*\n\n"
            f"📤 Zəhmət olmasa ödənişi etdikdən sonra çeki yükləyin.\n"
            f"Ödəniş yoxlanıldıqdan sonra abunəliyiniz aktiv ediləcək ✅"
        )
    else:
        text = "⚠️ Seçim tapılmadı."

    await query.message.reply_text(text, parse_mode="Markdown")
