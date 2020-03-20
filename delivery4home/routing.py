from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from telegram_bot.tasks import ConversationManagerTask

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "channel": ChannelNameRouter({
        "telegram-bot": ConversationManagerTask,
    }),
})