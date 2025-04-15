from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_live_matches, get_prematch_matches
from rapidfuzz import fuzz

async def live_match_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = await get_live_matches()
    if not matches:
        await update.message.reply_text("Hazırda canlı oyun yoxdur.")
        return

    message = "\U0001F4FA *Canlı Oyunlar:*\n\n"
    context.user_data["matches"] = []

    for idx, match in enumerate(matches[:10], start=1):
        home = match["home_team"]
        away = match["away_team"]
        time = match.get("time", "--:--")
        message += f"{idx}. {home} vs {away} ({time})\n"
        context.user_data["matches"].append({"match_id": match["id"]})

    await update.message.reply_text(message, parse_mode="Markdown")

async def prematch_match_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()
    all_matches = await get_prematch_matches()
    if not all_matches:
        await update.message.reply_text("Prematch oyun yoxdur.")
        return

    # Komanda adı uyğunluğuna görə filtr
    scored_matches = []
    for match in all_matches:
        home = match["home_team"]
        away = match["away_team"]
        teams_combined = f"{home} vs {away}"
        score = fuzz.ratio(user_input, teams_combined.lower())
        if score >= 60:
            scored_matches.append((score, match))

    # Vaxta görə sırala
    filtered = sorted(scored_matches, key=lambda x: x[1].get("start_time", ""))[:10]

    if not filtered:
        await update.message.reply_text("Uyğun prematch oyun tapılmadı.")
        return

    message = "\U0001F4C5 *Uyğun Prematch Oyunlar:*\n\n"
    context.user_data["matches"] = []

    for idx, (_, match) in enumerate(filtered, start=1):
        home = match["home_team"]
        away = match["away_team"]
        time = match.get("start_time", "--:--")
        message += f"{idx}. {home} vs {away} ({time})\n"
        context.user_data["matches"].append({"match_id": match["id"]})

    await update.message.reply_text(message, parse_mode="Markdown")
