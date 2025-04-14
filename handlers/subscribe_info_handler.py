from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import SUBSCRIPTION_PRICE

async def subscribe_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"🔐 *Abunəlik Xüsusiyyətləri:*\n\n"
        f"✔️ AI əsaslı oyun təhlilləri\n"
        f"✔️ Qeyri-səlis məntiqə əsaslanan mərc tövsiyələri\n"
        f"✔️ Sevimli komandaları izləmə\n"
        f"✔️ Kupon analizi\n\n"
        f"💳 *Qiymət:* {SUBSCRIPTION_PRICE}\n\n"
        f"Ödəniş metodunu seçmək üçün aşağıdakı düymələrdən istifadə edin:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 M10 ilə ödəniş", callback_data="pay_m10")],
        [InlineKeyboardButton("💳 Kartla ödəniş", callback_data="pay_card2card")]
    ])

    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=keyboard)
