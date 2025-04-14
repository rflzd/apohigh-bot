from telegram import Update
from telegram.ext import ContextTypes
from utils.flag_to_country import flag_to_country  # Əgər istifadə olunursa
from services.highlightly import get_leagues  # API-dən liqaları çəkən funksiya

async def league_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if not mode:
        return  # Heç bir seçim etməyibsə, cavab vermə

    country = flag_to_country(text) or text.strip().lower()
    context.user_data["country"] = country

    leagues = await get_leagues(mode=mode, country=country)
    if not leagues:
        await update.message.reply_text("Heç bir liqa tapılmadı. Başqa ölkə adı və ya bayraq göndərin.")
        return

    context.user_data["leagues"] = leagues
    msg = "Aşağıdakı liqalardan birini seçin:\n\n"
    msg += "\n".join([f"{idx+1}. {l['league_name']}" for idx, l in enumerate(leagues)])
    msg += "\n\nSadəcə nömrəni yazın (məs: 1)"

    await update.message.reply_text(msg)
