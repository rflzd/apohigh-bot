from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_match_detail

async def match_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text.isdigit():
        return

    matches = context.user_data.get("matches")
    if not matches:
        return

    idx = int(text) - 1
    if idx < 0 or idx >= len(matches):
        await update.message.reply_text("Yanlış seçim. Zəhmət olmasa düzgün nömrə daxil edin.")
        return

    selected_match = matches[idx]
    context.user_data["selected_match"] = selected_match

    match_id = selected_match["match_id"]
    match_data = await get_match_detail(match_id)

    if not match_data:
        await update.message.reply_text("Oyun detalları tapılmadı.")
        return

    msg = f"📊 *{match_data['home_team']} vs {match_data['away_team']}*\n"
    msg += f"🕒 {match_data['time']}\n"
    msg += f"📍 {match_data['league_name']}\n\n"
    msg += f"📈 Oranlar:\n"
    for odd in match_data.get("odds", []):
        msg += f" - {odd['type']}: {odd['value']}\n"

    await update.message.reply_text(msg, parse_mode="Markdown")
