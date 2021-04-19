import os
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
import requests
import vk_api

LOGIN = os.environ.get('login')
PASSWORD = os.environ.get('password')
OWNER_ID = os.environ.get('appID')


def generate_token():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    return dict(vk_session.token).get('access_token')


def copy_msg(bot: Bot, update: Update):
    text = update.channel_post.text
    token = generate_token()
    request = requests.get(f"https://api.vk.com/method/wall.post?owner_id={OWNER_ID}&from_group=1&"
                           f"message={text}&access_token={token}&v=5.130")
    request.close()
    data = request.json()
    print(data)


def main():
    bot = Bot(
        token=os.environ.get('TgVKBotToken'),
    )
    updater = Updater(bot=bot)
    message_handler = MessageHandler(Filters.text, copy_msg)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
