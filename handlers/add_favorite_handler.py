from telegram import Update
from telegram.ext import ContextTypes
from db.db import SessionLocal
from db.models.favorite_team import FavoriteTeam

async def add_favorite_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # İstifadəçinin komandası
    team_name = update.message.text.strip()
    
    # Veritabanında yoxlayırıq
    session = SessionLocal()
    existing_team = session.query(FavoriteTeam).filter_by(team_name=team_name).first()

    if existing_team:
        await update.message.reply_text(f"⚠️ Bu komanda artıq sevimli komandalarınıza əlavə olunub: {team_name}")
    else:
        # Yeni komanda əlavə edirik
        new_team = FavoriteTeam(team_name=team_name, user_id=update.message.from_user.id)
        session.add(new_team)
        session.commit()
        await update.message.reply_text(f"✅ {team_name} komandası sevimli komandalarınıza əlavə olundu.")
    
    session.close()
