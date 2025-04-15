from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_matches

async def match_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text.isdigit():
        return

    leagues = context.user_data.get("leagues")
    if not leagues:
        return

    idx = int(text) - 1
    if idx < 0 or idx >= len(leagues):
        await update.message.reply_text("Yanlış seçim. Zəhmət olmasa düzgün nömrə daxil edin.")
        return

    selected_league = leagues[idx]
    context.user_data["selected_league"] = selected_league

    # Fetch mode from user context
    mode = context.user_data.get("mode", "live")  # Default to live if no mode is set

    # Get matches based on selected mode and timezone Asia/Baku
    matches = await get_matches(
        mode=mode,
        league_id=selected_league["league_id"],
        timezone="Asia/Baku"  # Bakı zaman zonası
    )

    if not matches:
        await update.message.reply_text("Heç bir oyun tapılmadı.")
        return

    context.user_data["matches"] = matches
    msg = f"📋 {selected_league['league_name']} üçün oyunlar:\n\n"
    for idx, match in enumerate(matches):
        msg += f"{idx + 1}. {match['home_team']} vs {match['away_team']}\n"

    msg += "\nZəhmət olmasa baxmaq istədiyiniz oyunun nömrəsini yazın (məs: 2)"
    await update.message.reply_text(msg)
