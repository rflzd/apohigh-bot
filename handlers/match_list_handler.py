from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_matches
from db.models.user import User  # User modelini import edirik
from db.services.match_service import insert_matches  # insert_matches funksiyasını import edirik

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

    # Fetch mode from user context, defaulting to live
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

    # Matçları verilənlər bazasına əlavə edirik
    insert_matches(matches['data'])

    context.user_data["matches"] = matches['data']
    msg = f"📋 {selected_league['league_name']} üçün oyunlar:\n\n"
    for idx, match in enumerate(matches['data']):
        msg += f"{idx + 1}. {match['home_team']} vs {match['away_team']}\n"

    msg += "\nZəhmət olmasa baxmaq istədiyiniz oyunun nömrəsini yazın (məs: 2)"
    await update.message.reply_text(msg)

    # Sevimli komandalar və abunəlik yoxlaması
    user = User.get_user(update.message.from_user.id)
    if user and user.is_subscribed:  # Yalnız abunə olanlar üçün
        for match in matches['data']:
            if match["home_team"] in user.favorite_teams or match["away_team"] in user.favorite_teams:
                # Canlı oyun varsa, istifadəçiyə məlumat göndəririk
                await update.message.reply_text(
                    f"🎉 {user.full_name}, sevimli komandanızın oyunu başladı! \n{match['home_team']} vs {match['away_team']} - Canlı!"
                )
