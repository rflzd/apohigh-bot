from telegram import Update
from telegram.ext import ContextTypes
from services.highlightly import get_live_matches, get_prematch_matches
from rapidfuzz.fuzz import ratio

async def live_match_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = await get_live_matches()
    if not matches:
        await update.message.reply_text("Hazırda canlı oyun yoxdur.")
        return

    message = "\U0001F4FA *Canlı Oyunlar:*\n"

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

    scored_matches = []
    for match in all_matches:
        home = match["home_team"]
        away = match["away_team"]
        teams_combined = f"{home} vs {away}"
        score = ratio(user_input, teams_combined.lower())
        if score >= 60:
            scored_matches.append((score, match))

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

    from services.highlightly import get_match_detail, get_odds, get_h2h, get_lineups
    from db.db import SessionLocal
    from db.models.user import User

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