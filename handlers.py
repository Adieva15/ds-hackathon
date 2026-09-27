from telegram import Update
from telegram.ext import ContextTypes
from ai_coach import ai_fitness_coach
from user_data import get_user_data, update_user_workouts, get_user_workouts, add_user_goal
from keyboards import main_keyboard


# ===ОБРАБОТЧИКИ КОМАНД ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user_data(user.id, user.username, user.first_name)

    welcome = f"""
Привет {user.first_name}! 👋 

Я твой ИИ-тренер Spovatar! 🤖
Просто расскажи мне о своих тренировках, и я:
• 🏋️ Проанализирую твой прогресс
• 💬 Дам персональный совет  
• 🌟 Помогу с мотивацией
• 🎯 Напомню о целях

Выбери действие ниже 👇
    """
    await update.message.reply_text(welcome, reply_markup=main_keyboard())


async def handle_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Спрашиваем тип тренировки
    await update.message.reply_text(
        "Какой тип тренировки?\n\n"
        "🏃 Бег\n"
        "🚴 Велосипед\n"
        "🏊 Плавание"
    )
    context.user_data['waiting_workout_type'] = True


async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    workouts = get_user_workouts(user_id)

    response = await ai_fitness_coach(
        f"Пользователь спрашивает про свой прогресс. У него {workouts} тренировок. Оцени прогресс и мотивируй.",
        user_id
    )

    progress_text = f"📊 Твои тренировки: {workouts}\n\n{response}"
    await update.message.reply_text(progress_text)


async def handle_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Дай персональный фитнес-совет на основе моего прогресса. Будь конкретным.",
        user_id
    )

    await update.message.reply_text(f"💬 Совет тренера:\n\n{response}")


async def handle_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Дай мотивацию для продолжения тренировок. Будь эмоциональным и вдохновляющим.",
        user_id
    )

    await update.message.reply_text(f"🌟 Мотивация:\n\n{response}")


async def handle_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        "🎯 Какую фитнес-цель ты хочешь поставить?\n\n"
        "Например:\n"
        "• 'Пробежать 5 км без остановки'\n"
        "• 'Проплыть 500 метров'\n"
        "• 'Проехать 20 км на велосипеде'"
    )

    context.user_data['waiting_for_goal'] = True


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 Помощь по боту:

🏋️ *Записал тренировку* - отмечаешь факт тренировки
📊 *Мой прогресс* - смотрю твою статистику  
💬 *Совет тренера* - получаешь персональный совет
🌟 *Мотивация* - вдохновляю на новые свершения
🎯 *Поставить цель* - помогаю с целями

*Или просто пиши в чат:*
- "Сегодня бегал 5 км"
- "Плавал 30 минут" 
- "Как улучшить выносливость?"
- "Устал, нет мотивации"

Я все пойму и помогу! 💪
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка любых текстовых сообщений через ИИ"""
    user_id = update.effective_user.id
    user_text = update.message.text
    user = update.effective_user

    # Обработка выбора типа тренировки
    if context.user_data.get('waiting_workout_type'):
        workout_type = None
        if any(word in user_text.lower() for word in ['бег', 'run']):
            workout_type = "бег"
        elif any(word in user_text.lower() for word in ['велосипед', 'вело', 'bike']):
            workout_type = "велосипед"
        elif any(word in user_text.lower() for word in ['плавание', 'плыл', 'swim']):
            workout_type = "плавание"

        if workout_type:
            workouts_count = update_user_workouts(user_id, workout_type)
            response = await ai_fitness_coach(f"Завершил {workout_type}. Всего тренировок: {workouts_count}", user_id)
            await update.message.reply_text(f"✅ Записал {workout_type}! Всего: {workouts_count}\n\n{response}")
        else:
            await update.message.reply_text("Не понял тип тренировки. Выбери: бег, велосипед или плавание")

        context.user_data['waiting_workout_type'] = False
        return

    # Обработка постановки цели
    if context.user_data.get('waiting_for_goal'):
        try:
            add_user_goal(user_id, user_text)
            response = f"🎯 Отлично! Цель '{user_text}' сохранена!\n\nТеперь давай работать над её достижением! 💪"
            context.user_data['waiting_for_goal'] = False
        except Exception as e:
            response = "❌ Не удалось сохранить цель. Попробуй еще раз."
            context.user_data['waiting_for_goal'] = False

        await update.message.reply_text(response)
        return

    # Обычное сообщение - обрабатываем через ИИ
    response = await ai_fitness_coach(user_text, user_id)
    await update.message.reply_text(response)