import logging
from telegram.error import TelegramError
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
    photo_url = 'https://raw.githubusercontent.com/Secure-Messages/web3-telegram-bot/main/images/snake-token.png'  # Замените на ваш URL или file_id

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
        [InlineKeyboardButton("Play Game", callback_data='play_game')],
        [InlineKeyboardButton("Back", callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    try:
        # First delete the existing message
        await query.message.delete()
        # Then send a new message with the text and the options
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Please choose an option:',
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error(f"Failed to update the message: {str(e)}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to update the message.")

async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()

        game_url = "https://t.me/SlitherWeb3Bot/SlitherWeb3App"

        buttons = [
            [InlineKeyboardButton("Play Game 🎮", url=game_url)],
            [InlineKeyboardButton("Back to Start", callback_data='back_to_start')]
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        await query.edit_message_text(text="Click the button below to start playing the Snake game! 🐍🎮",
                                      reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Failed to launch the game or handle the query: {str(e)}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to launch the game.")

async def connect_ton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ton_connector = TonConnector()
    generated_url = await ton_connector.connect()

    # Create a button that directly opens the URL and a back button
    buttons = [
        [InlineKeyboardButton("Connect Now", url=generated_url)],
        [InlineKeyboardButton("Back", callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # Update the message to include the button
    try:
        await query.edit_message_text(
            text="Please click the button below to connect your wallet:",
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error(f"Failed to update the message for wallet connection: {str(e)}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to update the connection message.")


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    welcome_text = (
        "<b>Welcome to the Slither Token Bot!</b>\n"
        "Click <b>Start</b> to continue and learn how you can collect coins "
        "playing the exciting <i>Snake game</i>! 🎮🐍\n"
        "Collect as many coins as you can and earn Slither Tokens! 💰🔥"
    )
    buttons = [[InlineKeyboardButton("Start", callback_data='start')]]
    keyboard = InlineKeyboardMarkup(buttons)

    photo_url = 'https://raw.githubusercontent.com/Secure-Messages/web3-telegram-bot/main/images/snake-token.png'

    try:
        # Check if the message exists and attempt to delete
        if query.message:
            await query.message.delete()
            logging.info("Message deleted successfully.")
        else:
            logging.info("No message found to delete.")

        # Send a new message with the photo, text, and buttons
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_url,
            caption=welcome_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        logging.info("Start message sent successfully.")
    except Exception as e:
        logging.error(f"Failed to reset to start: {str(e)}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to return to the start.")








def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()


async def safe_execute(coroutine, update, context):
    try:
        await coroutine(update, context)
    except TelegramError as e:
        logging.error("Failed to execute handler: %s", str(e))
        # Optionally, send a message back to the user that something went wrong.
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred.")


def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        if query.data == 'start':
            asyncio.create_task(show_options(update, context))
        elif query.data == 'connect_ton':
            asyncio.create_task(connect_ton(update, context))
        elif query.data == 'play_game':
            asyncio.create_task(play_game(update, context))
        elif query.data == 'back':
            asyncio.create_task(back_to_start(update, context))
        elif query.data == 'back_to_start':  # Make sure this is correct and being called
            asyncio.create_task(back_to_start(update, context))
        else:
            logging.error(f"Unhandled callback data: {query.data}")
    except Exception as e:
        logging.error(f"Error handling button press: {str(e)}")


if __name__ == "__main__":
    run_telegram_bot()
