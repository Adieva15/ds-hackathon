# === НАСТРОЙКИ ===
import os
import logging
import base64


BOT_TOKEN = ''

# Настройки OpenAI
# OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_BASE_URL="https://ngw.devices.sberbank.ru:9443/api/v1/"
OPENAI_MODEL ='GigaChat-2-lite'

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client_id = ""
client_secret = ""

# Создаем строку для кодирования
credentials = f"{client_id}:{client_secret}"

AI_TOKEN = base64.b64encode(credentials.encode()).decode()

# print(f"Ваш AI_TOKEN: {AI_TOKEN}")
