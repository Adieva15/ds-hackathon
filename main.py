from telegram.ext import  Application, CommandHandler, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN, logger, WEB_APP_URL
from handlers import (
    start, handle_help, handle_workout, handle_progress,
    handle_advice, handle_motivation, handle_goal, handle_message
)
from telegram import Update, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
async def web_app_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Открыть тренера", web_app=WebAppInfo(url=WEB_APP_URL))
    ]])
    await update.message.reply_text("Запусти мини-приложение:", reply_markup=keyboard)


def setup_handlers(application):
    """Настройка всех обработчиков"""
    # Команды
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', handle_help))
    application.add_handler(CommandHandler('app', web_app_handler))

    # Обработчики кнопок
    application.add_handler(MessageHandler(filters.Regex('^🏋️ Записал тренировку$'), handle_workout))
    application.add_handler(MessageHandler(filters.Regex('^📊 Мой прогресс$'), handle_progress))
    application.add_handler(MessageHandler(filters.Regex('^💬 Совет тренера$'), handle_advice))
    application.add_handler(MessageHandler(filters.Regex('^🌟 Мотивация$'), handle_motivation))
    application.add_handler(MessageHandler(filters.Regex('^🎯 Поставить цель$'), handle_goal))
    application.add_handler(MessageHandler(filters.Regex('^🆘 Помощь$'), handle_help))

    # Обработка любых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    setup_handlers(application)

    print("🤖 Фитнес-бот запущен!")
    application.run_polling()


if __name__ == "__main__":
    main()