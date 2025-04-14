from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_match_details
from ai_analysis.analyzer import generate_ai_analysis
from db.db import SessionLocal
from db.models.user import User

async def match_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    selected_text = update.message.text
    matches = context.user_data.get("matches", [])

    # Uyğun oyunu tap
    selected_match = next((m for m in matches if selected_text in f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}"), None)
    
    if not selected_match:
        await update.message.reply_text("Uyğun oyun tapılmadı.")
        return

    match_id = selected_match["id"]
    match_info = get_match_details(match_id)

    if not match_info:
        await update.message.reply_text("Oyun detalları yüklənə bilmədi.")
        return

    match = match_info[0]
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    state = match["state"]
    start_time = match["startDate"]

    msg = f"📊 *{home} vs {away}*\n🕒 {start_time}\n📌 Status: {state}"
    await update.message.reply_text(msg, parse_mode="Markdown")

    # Abunəlik yoxlanışı
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if user and user.is_subscribed:
        ai_analysis = generate_ai_analysis(match)
        await update.message.reply_text(f"🤖 AI Analizi:\n{ai_analysis}", parse_mode="Markdown")
    else:
        await update.message.reply_text("🔒 AI analizi üçün abunə olun.")
