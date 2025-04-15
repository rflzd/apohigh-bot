from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from config import BOT_TOKEN, ADMIN_IDS
from handlers.start_handler import start_command
from handlers.mode_handler import mode_handler
from handlers.match_handler import (
    live_match_list_handler,
    prematch_match_list_handler,
    match_detail_handler
)
from handlers.favorites_handler import favorites_handler
from handlers.add_favorite_handler import add_favorite_handler
from handlers.bet_analysis_handler import bet_analysis_handler
from handlers.subscribe_info_handler import subscribe_info_handler
from handlers.payment_method_handler import payment_method_handler
from handlers.payment_upload_handler import payment_upload_handler
from handlers.admin_pending_handler import pending_payments_handler
from handlers.forward_to_admin_handler import forward_to_admin_handler

# Admin yoxlama funksiyası
async def admin_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Siz admin deyilsiniz. Bu funksiya yalnız adminlər üçün əlçatandır.")
        return False
    return True

# Bot obyektini yarat
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Komandalar
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("addfav", add_favorite_handler))
app.add_handler(CommandHandler("pending", pending_payments_handler))

# Admin komandaları
app.add_handler(CommandHandler("approve", approve_payment_handler))
app.add_handler(CommandHandler("pending", pending_payments_handler))

# Callback & media
app.add_handler(CallbackQueryHandler(forward_to_admin_handler, pattern="^forward_admin_"))
app.add_handler(CallbackQueryHandler(payment_method_handler, pattern="^pay_"))
app.add_handler(MessageHandler(filters.PHOTO, payment_upload_handler))

# Menü düymələri
app.add_handler(MessageHandler(filters.Regex("Abunə ol"), subscribe_info_handler))
app.add_handler(MessageHandler(filters.Regex("Sevimli komandalar 💖"), favorites_handler))
app.add_handler(MessageHandler(filters.Regex("Kupon analizi 🎯"), bet_analysis_handler))

# Oyun siyahıları (tablar)
app.add_handler(MessageHandler(filters.Regex("Canlı"), live_match_list_handler))
app.add_handler(MessageHandler(filters.Regex("Prematch"), prematch_match_list_handler))

# Oyun detalları
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), match_detail_handler))

# Botu işə sal
if __name__ == "__main__":
    print("🤖 Bot işə düşdü...")
    app.run_polling()
