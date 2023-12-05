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
import requests
from multiprocessing import Queue
from handlers import start, help_command, set_city, weather, choose_state, cancel
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext
from utils.constants import TELEGRAM_TOKEN, CHOOSING_STATE, BASE_ALERTS_API_URL, API_KEY, states

# * The alarm is received from this API https://alerts.com.ua/, it is planned to switch to the official API https://www.ukrainealarm.com/
def received_state(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text

    # Extract the selected state's ID from the user's input
    selected_state_id = next((state['id'] for state in states if f"({state['id']})" in user_input), None)

    if selected_state_id:
        # Construct the API URL using the selected state's ID
        state_api_url = f"{BASE_ALERTS_API_URL}{selected_state_id}"
        
        # Make API request with the constructed URL
        response = requests.get(state_api_url, headers={"X-API-Key": API_KEY})

        if response.status_code == 200:
            alert_data = response.json()
            alert_state = alert_data.get('state')
            if alert_state and alert_state.get('alert'):
                name = alert_state.get('name')
                update.message.reply_text(f"🚨 Увага! Повітряна тривога у {name}!")
            else:
                pass
        else:
            pass

        return ConversationHandler.END

    update.message.reply_text("Недійсний вибір області. Будь ласка, виберіть область із наданого списку.")
    return CHOOSING_STATE

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('choose_state', choose_state)],
        states={
            CHOOSING_STATE: [MessageHandler(filters.Text, received_state)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("set_city", set_city))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(conv_handler)

    # Set up a job to fetch alert data periodically
    job_queue = application.job_queue
    job_queue.run_repeating(received_state, interval=3600, first=0)

    application.run_polling()
    application.idle()

if __name__ == '__main__':
    main()
# End-of-file (EOF)
