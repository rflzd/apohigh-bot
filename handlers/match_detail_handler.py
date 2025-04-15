from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import (
    get_match_detail,
    get_odds,
    get_h2h,
    get_lineups
)
from db.db import SessionLocal
from db.models.user import User

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

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
    is_subscribed = getattr(user, "is_subscribed", False)
    session.close()

    match_data = await get_match_detail(match_id)
    if not match_data:
        await update.message.reply_text("Oyun detalları tapılmadı.")
        return

    msg = f"⚽ *{match_data['home_team']}* vs *{match_data['away_team']}*\n"
    msg += f"🕒 {match_data['time']}\n"
    msg += f"📍 {match_data['league_name']}"

    if is_subscribed:
        odds = await get_odds(match_id)
        h2h = await get_h2h(match_data['home_team_id'], match_data['away_team_id'])
        lineup = await get_lineups(match_id)

        if odds:
            msg += f"\n💸 *Əmsallar:*\n"
            for odd in odds.get("odds", []):
                msg += f" - {odd['type']}: {odd['value']}\n"

        if h2h:
            msg += f"\n📈 *Son Qarşılaşmalar (H2H):*\n"
            for game in h2h.get("matches", [])[:3]:
                msg += f" - {game['home']} {game['home_score']}:{game['away_score']} {game['away']} ({game['date']})\n"

        if lineup:
            msg += f"\n👥 *Heyətlərdən Seçmə:*\n"
            home_players = lineup.get("home_team", {}).get("players", [])[:2]
            away_players = lineup.get("away_team", {}).get("players", [])[:2]
            msg += " - " + ", ".join(p["name"] for p in home_players) + " (Home)\n"
            msg += " - " + ", ".join(p["name"] for p in away_players) + " (Away)\n"
    else:
        msg += "\n🔒 Əlavə statistika və AI təhlillər üçün abunə olun!"

    await update.message.reply_text(msg, parse_mode="Markdown")
