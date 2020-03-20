from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import threading
import enum
import time

CHAT_ID = None
UPDATER = None


class HelpMessagesThread(threading.Thread):
    @classmethod
    def send_help_messages(cls):
        global CHAT_ID
        global UPDATER

        reply_keyboard = [['Take', 'Cancel']]

        time.sleep(5)

        if UPDATER is not None:
            UPDATER.bot.send_message(CHAT_ID, 'Help needed in your area!')
            UPDATER.bot.send_message(CHAT_ID, 'Jack needs help in buying groceries')
            UPDATER.bot.send_location(CHAT_ID, 31.7625172, 35.2175533, reply_markup=ReplyKeyboardMarkup(reply_keyboard))

    def run(self) -> None:
        type(self).send_help_messages()


class RegistrationEnum(enum.Enum):
    NAME = 0
    LOCATION = enum.auto()
    PHONE_NUMBER = enum.auto()
    LANGUAGES = enum.auto()


def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat.id
    update.message.reply_text(f'Let\'s start, {update.message.from_user.first_name}!')

    return request_name(update, context)


def request_name(update, context):
    update.message.reply_text('What is your name ?', reply_markup=ReplyKeyboardRemove())
    return RegistrationEnum.NAME


def invalid_name(update, context):
    update.message.reply_text(f'Invalid name!')
    return request_name(update, context)


def name(update, context):
    update.message.reply_text('What is your location ?')
    return RegistrationEnum.LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    if user_location is not None:
        update.message.reply_text(f"Location of {user.first_name}: {user_location.latitude} / {user_location.longitude}")

    update.message.reply_text('What is your phone number ?')
    return RegistrationEnum.PHONE_NUMBER


def invalid_location(update, context):
    update.message.reply_text(f'Invalid location!')
    return name(update, context)


def skip_location(update, context):
    update.message.reply_text('Skipped location. What is you phone number?')
    return RegistrationEnum.PHONE_NUMBER


def phone_number(update, context):
    reply_keyboard = [['English', 'עברית', 'العربية', 'русский', 'français', 'Done']]

    update.message.reply_text(
        'Language?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )
    return RegistrationEnum.LANGUAGES


def invalid_phone_number(update, context):
    update.message.reply_text(f'Invalid phone number!')
    return location(update, context)


def skip_phone_number(update, context):
    reply_keyboard = [['English', 'עברית', 'العربية', 'русский', 'français', 'Done']]

    update.message.reply_text(
        'Skipped phone number. Language?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )
    return RegistrationEnum.LANGUAGES


def language(update, context):
    reply_keyboard = [['English', 'עברית', 'العربية', 'русский', 'français', 'Done']]

    update.message.reply_text(
        'Any more language speaking?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )

    return RegistrationEnum.LANGUAGES


def language_done(update, context):
    global CHAT_ID

    update.message.reply_text(
        'Registration success',
        reply_markup=ReplyKeyboardRemove()
    )
    help_message_thread = HelpMessagesThread()
    help_message_thread.run()

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Aborted')
    return ConversationHandler.END


def main():
    global UPDATER

    with open('token.txt', 'rt') as f:
        UPDATER = Updater(f.read(), use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RegistrationEnum.NAME: [
                MessageHandler(Filters.regex(r'^[a-zA-Zא-ת]+(([\',. -][a-zA-Zא-ת ])?[a-zA-Zא-ת]*)*$'), name),
                MessageHandler(filters=None, callback=invalid_name),
            ],
            RegistrationEnum.LOCATION: [
                MessageHandler(Filters.location, location), CommandHandler('skip', skip_location),
                MessageHandler(filters=None, callback=invalid_location),
            ],
            RegistrationEnum.PHONE_NUMBER: [
                MessageHandler(Filters.regex(r'^05\d([-]{0,1})\d{7}$'), phone_number),
                MessageHandler(filters=None, callback=invalid_phone_number),
            ],
            RegistrationEnum.LANGUAGES: [
                MessageHandler(filters=Filters.regex('^(Done|No)$'), callback=language_done),
                MessageHandler(Filters.regex(r'^.*$'), language),
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    UPDATER.dispatcher.add_handler(conv_handler)

    UPDATER.start_polling()
    UPDATER.idle()


if __name__ == '__main__':
    print('Starting telegram server...')
    main()
