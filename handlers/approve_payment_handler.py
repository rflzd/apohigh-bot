from telegram import Update
from telegram.ext import ContextTypes

async def approve_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Burada ödənişin təsdiqinə dair funksionallıq olacaq
    # Bu, sadə bir təsdiqləmə mesajıdır
    await update.message.reply_text("Ödəniş təsdiqləndi!")
