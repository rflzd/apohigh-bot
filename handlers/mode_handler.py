from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "canlı" in text:
        context.user_data["mode"] = "live"
        await update.message.reply_text("🇺🇳 Hansı ölkənin liqasını izləmək istəyirsiniz? Bayraq göndərin və ya ad yazın.")
    elif "prematch" in text:
        context.user_data["mode"] = "prematch"
        await update.message.reply_text("🇺🇳 Hansı ölkənin liqasını izləmək istəyirsiniz? Bayraq göndərin və ya ad yazın.")
    else:
        await update.message.reply_text("Zəhmət olmasa 'Canlı' və ya 'Prematch' seçimlərindən birini edin.")
