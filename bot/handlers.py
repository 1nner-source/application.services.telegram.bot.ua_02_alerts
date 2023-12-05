"""Handlers Module for Telegram Bot

This module contains the command and message handlers used in the Telegram bot. It includes
functions to handle various commands, messages, and conversation flows within the bot.

Functions:
    - start(update, context): Handles the /start command.
    - help_command(update, context): Handles the /help command.
    - set_city(update, context): Handles setting the user's city for weather updates.
    - weather(update, context): Retrieves weather updates for the user's city.
    - choose_state(update, context): Initiates the state selection conversation flow.
    - received_state(update, context): Handles user's state selection in the conversation.
    - cancel(update, context): Handles cancelling the ongoing conversation.

Example Usage:
    These functions are utilized as command and message handlers in the bot's main logic. They're
    added to the dispatcher to respond to specific commands or messages. For instance:

        - Adding 'start' command handler in 'bot.py':
            `dispatcher.add_handler(CommandHandler("start", start))`

        - Implementing a conversation handler using 'choose_state' and 'received_state' functions.

Note:
    The handlers in this module are integrated with the Telegram bot's functionality and are invoked
    based on user commands, messages, or conversation flow triggers.
"""
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import  ConversationHandler, CallbackContext
from utils.constants import WEATHER_API_KEY, states, CHOOSING_STATE

def start(update: Update) -> None:
    """Start the bot"""
    update.message.reply_text('Привіт! Я твій універсальний бот. Напиши /help щоб подивитись доступні команди.')

def help_command(update: Update) -> None:
    """Help commands"""
    update.message.reply_text('Ви можете використовувати наступні команди:\n'
                              '/start - Запустити бота\n'
                              '/help - Отримати допомогу\n'
                              '/alert - Активувати сповіщення'
                              '/set_city <city_name> - Налаштуйте своє місто для оновлення погоди\n'
                              '/weather - Отримуйте оновлення погоди у вашому місті'
                              '/choose_state - Оберіть вашу область')
    
def choose_state(update: Update) -> int:
    """Function to set the user state"""
    keyboard = [
        [f"{state['name']} ({state['id']})"] for state in states
    ]
    update.message.reply_text(
        "Будь ласка оберіть свою область:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_STATE    

def set_city(update: Update, context: CallbackContext) -> None:
    """Function to set the user city"""
    city = ' '.join(context.args)
    if city:
        context.user_data['city'] = city
        update.message.reply_text(f'Ваше місто налаштовано на {city}')
    else:
        update.message.reply_text('Укажіть дійсну назву міста')

def weather(update: Update, context: CallbackContext) -> None:
    """Trigger the fetch_data to get the weather data"""
    if 'city' in context.user_data:
        city = context.user_data['city']
        # Here, you can trigger the job with the city information
        context.job_queue.run_once(fetch_data, 0, context=update.message.chat_id, city=city)
        update.message.reply_text(f"Отримання оновленої інформації про погоду для {city}...")
    else:
        update.message.reply_text('Будь ласка, встановіть своє місто за допомогою команди /set_city')

# * Test function for obtaining weather data for the city selected by the user.
# * This api doesn't work with such parameters, because it's' not the city that needs to be transferred,
# * but rather its longitude/latitude parameters
def fetch_data(context: CallbackContext) -> None:
    """Fetch the weather data from API"""
    job = context.job
    if 'city' in job.context:  # Check if 'city' data is already stored in job context
        city = job.context['city']
        weather_api_url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(weather_api_url, timeout=10)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['current']['temp_c']
            context.bot.send_message(job.context['chat_id'], f"Поточна температура в {city} - {temperature}°C.")
        else:
            context.bot.send_message(job.context['chat_id'], 'Не вдалося отримати дані про погоду.')
    else:
        context.bot.send_message(job.context['chat_id'], 'Для отримання погоди не вказано місто.')

def cancel(update: Update) -> int:
    """Function to cancel tje Conversation Handler"""
    update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
# End-of-file (EOF)
