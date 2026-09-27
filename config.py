
import os
import logging
import base64


BOT_TOKEN = ''

# Настройки OpenAI
# OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_BASE_URL="https://ngw.devices.sberbank.ru:9443/api/v1/"
OPENAI_MODEL ='GigaChat-2-lite'
BOT_TOKEN=''

GIGACHAT_TOKEN = ""  # Полученный токен или путь к файлу с токеном
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"  # Область доступа
GIGACHAT_MODEL = "GigaChat-2-Max"

DATABASE_URL='sqlite:///fitness_bot.db'

WEB_APP_URL = 'https://Adievadine.pythonanywhere.com'
# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)


client_id = ""
client_secret = ""

# Создаем строку для кодирования
credentials = f"{client_id}:{client_secret}"

AI_TOKEN = base64.b64encode(credentials.encode()).decode()

# print(f"Ваш AI_TOKEN: {AI_TOKEN}")
