from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_leagues_by_country
from utils.flags import extract_country_name_from_flag

async def league_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    country_name = input_text

    # Əgər bayraq göndəribsə, onu ölkə adına çevir
    if any(char in input_text for char in range(0x1F1E6, 0x1F1FF)):
        country_name = extract_country_name_from_flag(input_text)

    if not country_name:
        await update.message.reply_text("Ölkə adı və ya bayraq düzgün deyil. Yenidən yoxlayın.")
        return

    leagues = get_leagues_by_country(country_name)

    if not leagues:
        await update.message.reply_text(f"'{country_name}' üçün heç bir liqa tapılmadı.")
        return

    keyboard = [[league['name']] for league in leagues]
    context.user_data["country"] = country_name
    context.user_data["leagues"] = leagues

    await update.message.reply_text(
        f"{country_name} üçün mövcud liqalar:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
