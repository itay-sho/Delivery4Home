from telegram.ext import Updater, CommandHandler
from volunteers.models import *
from channels.consumer import SyncConsumer
from volunteers.models import Volunteer


class TelegramTask(SyncConsumer):
    @staticmethod
    def hello(update, context):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    @staticmethod
    def start(update, context):
        found = True

        try:
            volunteer = Volunteer.objects.get(telegram_user_id=update.message.from_user.id)
        except Exception as e:
            found = False

        if found:
            update.message.reply_text(f'Welcome back, {update.message.from_user.first_name}!')
        else:
            update.message.reply_text(
                f'let\'s start, {update.message.from_user.first_name}, {update.message.from_user.id}!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('woot')
        with open('token.txt', 'rt') as f:
            updater = Updater(f.read(), use_context=True)

        updater.dispatcher.add_handler(CommandHandler('hello', TelegramTask.hello))
        updater.dispatcher.add_handler(CommandHandler('start', TelegramTask.start))

        updater.start_polling()
        updater.idle()

    async def run_bot(self, message):
        print('hi')
