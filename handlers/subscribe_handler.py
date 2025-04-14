from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes
from utils.config import TELEGRAM_PROVIDER_TOKEN

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    await update.callback_query.message.reply_invoice(
        title="Apohigh Abunəlik",
        description="1 aylıq premium abunəlik",
        payload="apohigh_subscription",
        provider_token=TELEGRAM_PROVIDER_TOKEN,
        currency="USD",
        prices=[LabeledPrice("1 aylıq abunəlik", 300 * 100)],
        start_parameter="subscribe"
    )
