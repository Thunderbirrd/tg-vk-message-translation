import os
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
import requests
import vk_api
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

LOGIN = str(os.environ.get('login'))
PASSWORD = str(os.environ.get('password'))
OWNER_ID = str(os.environ.get('appID'))
PORT = int(os.environ.get('PORT', 8443))
TOKEN = str(os.environ.get('TgVKBotToken'))


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


def main():
    try:
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
    except Exception as e:
        logger.error(type(e))
        logger.error(e.args)
        logger.error(e)


if __name__ == '__main__':
    main()
