from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.api import get_matches_by_league_name

async def match_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    league_name = update.message.text
    mode = context.user_data.get("mode")

    matches = get_matches_by_league_name(league_name, mode)

    if not matches:
        await update.message.reply_text("Bu liqa üçün uyğun oyun tapılmadı.")
        return

    context.user_data["matches"] = matches

    # Oyun siyahısı keyboard
    keyboard = []
    for match in matches:
        title = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
        keyboard.append([title])

    await update.message.reply_text(
        "Oyunlardan birini seçin:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
