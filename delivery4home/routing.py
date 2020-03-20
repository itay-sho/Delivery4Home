from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from telegram_bot.tasks import TelegramTask

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "channel": ChannelNameRouter({
        "telegram-task": TelegramTask,
    }),
})