from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from config import BOT_TOKEN
from handlers.start_handler import start_command
from handlers.mode_handler import mode_handler
from handlers.league_handler import league_handler
from handlers.match_list_handler import match_list_handler
from handlers.match_detail_handler import match_detail_handler
from handlers.favorites_handler import favorites_handler
from handlers.add_favorite_handler import add_favorite_handler
from handlers.bet_analysis_handler import bet_analysis_handler
from handlers.subscribe_info_handler import subscribe_info_handler
from handlers.payment_method_handler import payment_method_handler
from handlers.payment_upload_handler import payment_upload_handler
from handlers.admin_pending_handler import pending_payments_handler
from handlers.forward_to_admin_handler import forward_to_admin_handler

# Bot obyektini yarat
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Komandalar
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("addfav", add_favorite_handler))
app.add_handler(CommandHandler("pending", pending_payments_handler))

# Callback & media
app.add_handler(CallbackQueryHandler(forward_to_admin_handler, pattern="^forward_admin_"))
app.add_handler(CallbackQueryHandler(payment_method_handler, pattern="^pay_"))
app.add_handler(MessageHandler(filters.PHOTO, payment_upload_handler))

# Menü düymələri
app.add_handler(MessageHandler(filters.Regex("Abunə ol"), subscribe_info_handler))
app.add_handler(MessageHandler(filters.Regex("Sevimli komandalar 💖"), favorites_handler))
app.add_handler(MessageHandler(filters.Regex("Kupon analizi 🎯"), bet_analysis_handler))
app.add_handler(MessageHandler(filters.Regex("^(⚽ Canlı|📅 Prematch)$"), mode_handler))

# Əsas oyun axını
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), league_handler))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), match_list_handler))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), match_detail_handler))

# Botu işə sal
if __name__ == "__main__":
    print("🤖 Bot işə düşdü...")
    app.run_polling()
