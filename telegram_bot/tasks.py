import channels
from telegram.ext import Updater, CommandHandler
from volunteers.models import *
from channels.consumer import SyncConsumer
import time


class ConversationManagerTask(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        while True:
            print(1)
            time.sleep(1)


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def start(update, context):
    volunteer = Volunteer.objects.get(update.message.from_user.id)

    if volunteer is None:
        update.message.reply_text(f'let\'s start, {update.message.from_user.first_name}, {update.message.from_user.id}!')
    else:
        update.message.reply_text(f'Welcome back, {update.message.from_user.first_name}!')


def main():
    with open('token.txt', 'rt') as f:
        updater = Updater(f.read(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
