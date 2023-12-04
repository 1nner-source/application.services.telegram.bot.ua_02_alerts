from multiprocessing import Queue
from handlers import start, help_command, set_city, weather, choose_state, received_state, cancel
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, filters
from utils.constants import TELEGRAM_TOKEN


# Conversation states
CHOOSING_STATE, TYPING_REPLY = range(2)

def main() -> None:
    update_queue = Queue()
    updater = Updater(TELEGRAM_TOKEN, update_queue=update_queue)
    # dispatcher = updater.dispatcher

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

    # Set up a job to fetch alert data periodically
    job_queue = updater.job_queue
    job_queue.run_repeating(received_state, interval=3600, first=0, context={'state_id': None, 'chat_id': None})

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()