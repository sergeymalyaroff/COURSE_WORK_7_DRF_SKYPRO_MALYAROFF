#COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/telegram_bot.py

from telegram.ext import Updater, CommandHandler

def start(update, context):
    """
    Обработчик команды /start.
    Вызывается, когда пользователь отправляет команду /start.
    Отправляет приветственное сообщение пользователю.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я ваш бот для отслеживания привычек.")

def help_command(update, context):
    """
    Обработчик команды /help.
    Вызывается, когда пользователь отправляет команду /help.
    Отправляет пользователю информацию о том, как использовать бота.
    """
    update.message.reply_text('Используйте /start для начала работы с ботом.')

def send_habit_notification(bot, chat_id, message):
    """
    Отправляет уведомление о привычке пользователю.
    :param bot: Экземпляр бота.
    :param chat_id: ID чата пользователя.
    :param message: Сообщение для отправки.
    """
    bot.send_message(chat_id=chat_id, text=message)

def main():
    """
    Основная функция для запуска бота.
    Создает экземпляр Updater и добавляет обработчики команд.
    """
    updater = Updater(token='TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
