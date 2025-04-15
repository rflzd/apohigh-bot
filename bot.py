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
app.add_handler(MessageHandler(filters.Regex("Canlı"), live_match_list_handler))
app.add_handler(MessageHandler(filters.Regex("Prematch"), prematch_match_list_handler))

async def main_flow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "league_stage" not in context.user_data:
        await league_handler(update, context)
        context.user_data["league_stage"] = "shown"
    elif "match_list_stage" not in context.user_data:
        await match_list_handler(update, context)
        context.user_data["match_list_stage"] = "shown"
    else:
        await match_detail_handler(update, context)
        context.user_data.clear()  # sıfırla axının sonu üçün

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), main_flow_handler))

# Botu işə sal
if __name__ == "__main__":
    print("🤖 Bot işə düşdü...")
    app.run_polling()
