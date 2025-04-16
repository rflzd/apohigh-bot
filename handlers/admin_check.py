from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS

async def admin_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Siz admin deyilsiniz. Bu funksiya yalnız adminlər üçün əlçatandır.")
        return False
    return True
