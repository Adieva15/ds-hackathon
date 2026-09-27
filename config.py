# === НАСТРОЙКИ ===
import os

# Токены
AI_TOKEN = ''
BOT_TOKEN = ''

# Настройки OpenAI
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_MODEL = "x-ai/grok-4.1-fast:free"

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

