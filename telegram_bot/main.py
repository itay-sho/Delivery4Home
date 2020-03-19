from telegram.ext import Updater, CommandHandler


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def start(update, context):
    update.message.reply_text('let\'s start, {}!'.format(update.message.from_user.first_name))


def main():
    with open('token.txt', 'rt') as f:
        updater = Updater(f.read(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
