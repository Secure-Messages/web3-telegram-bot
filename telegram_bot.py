import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from ton_connector import TonConnector
import asyncio
from config import TELEGRAM_TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "<b>Welcome to the Slither Token Bot!</b>\n"
        "Click <b>Start</b> to continue and learn how you can collect coins "
        "playing the exciting <i>Snake game</i>! 🎮🐍\n"
        "Collect as many coins as you can and earn Slither Tokens! 💰🔥"
    )
    buttons = [[InlineKeyboardButton("Start", callback_data='start')]]
    keyboard = InlineKeyboardMarkup(buttons)

    # Указание на URL изображения или file_id
    photo_url = '../images/snake-token.png'  # Замените на ваш URL или file_id

    await update.message.reply_photo(
        photo=photo_url,
        caption=welcome_text,
        parse_mode='HTML',
        reply_markup=keyboard
    )

async def show_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton("Connect to TON", callback_data='connect_ton')],
        [InlineKeyboardButton("Back", callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(text='Please choose an option:', reply_markup=keyboard)

async def connect_ton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ton_connector = TonConnector()
    generated_url = await ton_connector.connect()
    await query.edit_message_text(text=f'Please connect your wallet using this link: {generated_url}')

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [[InlineKeyboardButton("Start", callback_data='start')]]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(text='Welcome back! Click Start to continue.', reply_markup=keyboard)

def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'start':
        asyncio.create_task(show_options(update, context))
    elif query.data == 'connect_ton':
        asyncio.create_task(connect_ton(update, context))
    elif query.data == 'back':
        asyncio.create_task(back_to_start(update, context))

def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
