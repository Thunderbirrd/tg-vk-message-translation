import os
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
import requests
from token import generate_token


LOGIN = str(os.environ.get('login'))
PASSWORD = str(os.environ.get('password'))
OWNER_ID = int(os.environ.get('communityID')) * (-1)
PORT = int(os.environ.get('PORT', 8443))
TOKEN = str(os.environ.get('TgVKBotToken'))


def copy_msg(bot: Bot, update: Update):
    text = update.channel_post.text
    token = generate_token(LOGIN, PASSWORD)
    request = requests.get(f"https://api.vk.com/method/wall.post?owner_id={OWNER_ID}&from_group=1&"
                           f"message={text}&access_token={token}&v=5.130")
    request.close()
    data = request.json()


def main():
    bot = Bot(
        token=TOKEN,
    )
    updater = Updater(bot=bot)
    message_handler = MessageHandler(Filters.text, copy_msg)
    updater.dispatcher.add_handler(message_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(f'https://tg-vk-message.herokuapp.com/{TOKEN}')
    updater.idle()


if __name__ == '__main__':
    main()
