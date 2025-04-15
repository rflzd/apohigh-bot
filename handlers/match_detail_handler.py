from telegram import Update
from telegram.ext import ContextTypes

async def match_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # İstifadəçinin göndərdiyi mesajı əldə edirik
    match_number = update.message.text

    # İstifadəçi tərəfindən seçilmiş oyunun nömrəsi ilə uyğun məlumatı tapırıq
    matches = context.user_data.get("matches", [])
    
    # Seçimlə uyğun olan oyunun tapılmaması vəziyyəti
    if not match_number.isdigit() or int(match_number) < 1 or int(match_number) > len(matches):
        await update.message.reply_text("Yanlış seçim, zəhmət olmasa düzgün oyunun nömrəsini daxil edin.")
        return
    
    # Oyunun təfərrüatlarını əldə edirik
    selected_match = matches[int(match_number) - 1]

    # Oyun haqqında məlumatları hazırlayırıq
    match_details = f"⚽ Oyun Detalları:\n\n"
    match_details += f"🏠 Ev Sahibi: {selected_match['home_team']}\n"
    match_details += f"🏟️ Qonaq: {selected_match['away_team']}\n"
    match_details += f"🕒 Tarix və Vaxt: {selected_match['match_time']}\n"
    match_details += f"🔴 Ev sahibi komanda statusu: {selected_match['home_team_status']}\n"
    match_details += f"🔴 Qonaq komanda statusu: {selected_match['away_team_status']}\n"

    # Digər oyun detallarını da əlavə edə bilərsiniz (score, oyunçular, statistika və s.)

    # Oyun təfərrüatlarını istifadəçiyə göndəririk
    await update.message.reply_text(match_details)
