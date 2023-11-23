#COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/telegram_bot.py

from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я ваш бот для отслеживания привычек.")

def help_command(update, context):
    update.message.reply_text('Используйте /start для начала работы с ботом.')

def main():
    updater = Updater(token='TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
