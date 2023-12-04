"""Telegram Bot Main Script

This script initializes and runs the Telegram bot. It sets up the bot's functionality by defining
command handlers, message handlers, conversation handlers, and other components necessary for the bot
to interact with users on the Telegram platform.

Functionality:
    - Initializes the bot using the Telegram Bot API token.
    - Defines various handlers to respond to user commands and messages.
    - Implements conversation flows for complex interactions using ConversationHandler.
    - Sets up periodic jobs for fetching weather updates and alert data.

Components:
    - main(): The main function that sets up the bot, initializes handlers, and starts the bot.

Example Usage:
    To run the bot, execute this script. Ensure the correct Telegram Bot API token is set in the TOKEN
    constant within this script.

    For instance:
        $ python bot.py

Note:
    Ensure sensitive information like API tokens, keys, or any credentials are kept secure and not
    exposed publicly in repositories or shared environments.
"""
from multiprocessing import Queue
from handlers import start, help_command, set_city, weather, choose_state, received_state, cancel
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, filters
from utils.constants import TELEGRAM_TOKEN, CHOOSING_STATE

def main() -> None:
    update_queue = Queue()
    updater = Updater(TELEGRAM_TOKEN, update_queue=update_queue)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('choose_state', choose_state)],
        states={
            CHOOSING_STATE: [MessageHandler(filters.Text & filters.Command, received_state)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater.add_handler(CommandHandler("start", start))
    updater.add_handler(CommandHandler("help", help_command))
    updater.add_handler(CommandHandler("set_city", set_city))
    updater.add_handler(CommandHandler("weather", weather))
    updater.add_handler(conv_handler)

    # Set up a job to fetch alert data periodically
    job_queue = updater.job_queue
    job_queue.run_repeating(received_state, interval=3600, first=0, context={'state_id': None, 'chat_id': None})

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()