import os
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
import requests
import vk_api
import logging

LOGIN = os.environ.get('login')
PASSWORD = os.environ.get('password')
OWNER_ID = os.environ.get('appID')
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('TgVKBotToken')


def generate_token():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    return dict(vk_session.token).get('access_token')


def copy_msg(bot: Bot, update: Update):
    try:
        text = update.channel_post.text
        token = generate_token()
        request = requests.get(f"https://api.vk.com/method/wall.post?owner_id={OWNER_ID}&from_group=1&"
                               f"message={text}&access_token={token}&v=5.130")
        request.close()
        data = request.json()
        print(data)
    except Exception:
        bot.send_message(chat_id=439349318, text="Fuck")


def main():
    bot = Bot(
        TOKEN,
    )
    updater = Updater(bot=bot, use_context=True)
    message_handler = MessageHandler(Filters.text, copy_msg)
    updater.dispatcher.add_handler(message_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://tg-vk-message.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
