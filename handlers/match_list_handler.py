from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_matches
from db.models.user import User  # User modelini import edirik
from db.services.match_service import insert_matches  # insert_matches funksiyasini import edirik

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

    mode = context.user_data.get("mode", "live")  # Default "live"

    matches = await get_matches(
        mode=mode,
        league_id=selected_league["league_id"],
        timezone="Asia/Baku"
    )

    if not matches:
        await update.message.reply_text("Heç bir oyun tapılmadı.")
        return

    context.user_data["matches"] = matches
    insert_matches(matches)  # Matçları database-ə yaz

    msg = f"📋 {selected_league['league_name']} üçün oyunlar:\n\n"
    for idx, match in enumerate(matches):
        msg += f"{idx + 1}. {match['home_team']} vs {match['away_team']}\n"

    msg += "\nZəhmət olmasa baxmaq istədiyiniz oyunun nömrəsini yazın (məs: 2)"
    await update.message.reply_text(msg)

    user = User.get_user(update.message.from_user.id)
    if user and user.is_subscribed:
        for match in matches:
            if match["home_team"] in user.favorite_teams or match["away_team"] in user.favorite_teams:
                await update.message.reply_text(
                    f"🎉 {user.full_name}, sevimli komandanızın oyunu başladı! \n{match['home_team']} vs {match['away_team']} - Canlı!"
                )
