"""Constants Module for Telegram Bot Configuration

This module contains constant values used throughout the Telegram bot application,
including API tokens, URLs, and other configuration settings.

Constants:
    - TOKEN (str): The Telegram Bot API token used for bot authentication.
    - WEATHER_API_KEY (str): API key for accessing the weather data API.
    - BASE_ALERTS_API_URL (str): Base URL for the alerts API.
    - API_KEY (str): API key for authentication in a specific service.
    - STATES (list): List of states with their IDs and names for user selection.

Example Usage:
    This module is imported wherever constant values are required in the bot's logic.
    For instance:
        - To set up the Telegram bot token in 'bot.py':
            `from utils.constants import TOKEN`

        - Accessing the list of states in a conversation handler in 'handlers.py':
            `from utils.constants import STATES`

Note:
    Ensure that sensitive information like API keys is kept secure and not exposed
    publicly in repositories or shared environments.
"""
TELEGRAM_TOKEN = "6806775714:AAGMrkaX2MCzzbWnm02TsCCxWesOXZ-qImo"
# WEATHER_API_KEY = "YOUR_WEATHER_KEY"
BASE_ALERTS_API_URL = "https://alerts.com.ua/api/states/"
STATES_API_URL = "https://alerts.com.ua/api/states"
API_KEY = "ca29e337:10c84d834be5fca13b2f9a8c53d80d29"

# Conversation states
CHOOSING_STATE, TYPING_REPLY = range(2)

# List of states with their names and IDs
states = [
    {"id": 1, "name": "Волинська область"},
    {"id": 2, "name": "Вінницька область"},
    {"id": 3, "name": "Дніпропетровська область"},
    {"id": 4, "name": "Донецька область"},
    {"id": 5, "name": "Житомирьска область"},
    {"id": 6, "name": "Закарпатська область"},
    {"id": 7, "name": "Запорізька область"},
    {"id": 8, "name": "Івано-Франківська область"},
    {"id": 9, "name": "Київська область"},
    {"id": 10, "name": "Кіровоградська область"},
    {"id": 11, "name": "Луганська область"},
    {"id": 12, "name": "Львівська область"},
    {"id": 13, "name": "Миколаївська область"},
    {"id": 14, "name": "Одеська область"},
    {"id": 15, "name": "Полтавська область"},
    {"id": 16, "name": "Рівненьска область"},
    {"id": 17, "name": "Сумська область"},
    {"id": 18, "name": "Тернопільска область"},
    {"id": 19, "name": "Харківська область"},
    {"id": 20, "name": "Херсонська область"},
    {"id": 21, "name": "Хмельницька область"},
    {"id": 22, "name": "Черкаська область"},
    {"id": 23, "name": "Чернівецька область"},
    {"id": 24, "name": "Чернігівська область"}
]
# End-of-file (EOF)
