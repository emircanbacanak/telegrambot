import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

TOKEN = "7619371697:AAEdRGFILRWY0TP5pfA0W7gkBiOJhOmSaJM"  # Bot ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

main_keyboard = [
    ["EUR/USD(OTC)", "EUR/GBP(OTC)"],
    ["EUR/CAD(OTC)", "EUR/JPY(OTC)"],
    ["GBP/USD(OTC)", "GBP/AUD(OTC)"],
    ["GBP/CHF(OTC)", "USD/CHF(OTC)"],
    ["USD/CAD(OTC)"]
]
main_reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True, one_time_keyboard=True)

signal_keyboard = [
    ["New Signal", "Back"]
]
signal_reply_markup = ReplyKeyboardMarkup(signal_keyboard, resize_keyboard=True, one_time_keyboard=True)

STICKER_ID = "CAACAgQAAxkBAAEyxZFn2QG2GkBRQQ9ji5974_t3llmhlQACOxgAAv8JyVJlrX8Imf7G1zYE"
STICKER_ID2 = "CAACAgQAAxkBAAEyxZNn2QHixuBaSUgGOMns3zcodCPHtQACYRUAArRMyFKY6WGTpmO2xDYE"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Bir OTC döviz çifti seçin:", reply_markup=main_reply_markup)

async def send_signal(update: Update, context: CallbackContext) -> None:
    result = random.choice(["⬆️", "⬇️"])
    if result == "⬆️":
        await context.bot.send_sticker(chat_id=update.message.from_user.id, sticker=STICKER_ID)
    else:
        await context.bot.send_sticker(chat_id=update.message.from_user.id, sticker=STICKER_ID2)

    await context.bot.send_message(
        chat_id=update.message.from_user.id,
        text="Lütfen bir seçenek seçin:",
        reply_markup=signal_reply_markup
    )

async def handle_selection(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    main_options = [item for sublist in main_keyboard for item in sublist]

    if text in main_options:
        await send_signal(update, context)
    elif text == "Back":
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text="Bir OTC döviz çifti seçin:",
            reply_markup=main_reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text="Lütfen geçerli bir seçenek seçin.",
            reply_markup=main_reply_markup
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selection))
    app.run_polling()
