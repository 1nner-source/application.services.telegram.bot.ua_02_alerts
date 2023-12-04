from handlers import start, help_command, set_city, weather, choose_state, received_state, cancel
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from utils.constants import TELEGRAM_TOKEN

# Conversation states
CHOOSING_STATE, TYPING_REPLY = range(2)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('choose_state', choose_state)],
        states={
            CHOOSING_STATE: [MessageHandler(Filters.text & ~Filters.command, received_state)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("set_city", set_city))
    dispatcher.add_handler(CommandHandler("weather", weather))

    # Set up a job to fetch alert data periodically
    job_queue = updater.job_queue
    job_queue.run_repeating(received_state, interval=3600, first=0, context={'state_id': None, 'chat_id': None})

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()