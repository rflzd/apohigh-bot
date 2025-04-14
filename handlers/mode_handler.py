from telegram import Update
from telegram.ext import ContextTypes

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "⚽ Canlı":
        context.user_data["mode"] = "live"
        await update.message.reply_text("🇦🇿 Zəhmət olmasa izləmək istədiyiniz ölkənin adını və ya bayrağını göndərin:")
    elif text == "📅 Prematch":
        context.user_data["mode"] = "prematch"
        await update.message.reply_text("🇹🇷 Zəhmət olmasa izləmək istədiyiniz ölkənin adını və ya bayrağını göndərin:")
