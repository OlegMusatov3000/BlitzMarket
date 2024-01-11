import traceback

import telegram

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, logger

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message_to_telegram(message, bot=bot):
    try:
        bot.send_message(
            TELEGRAM_CHAT_ID,
            f"произошла ошибка: {message}\n {traceback.format_exc()}"
        )
        logger.info("Сообщение с критической ошибкой отправлено в телеграм")

    except telegram.TelegramError as error:
        logger.error(f"{error}\n{traceback.format_exc()}")
