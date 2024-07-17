import os
import urllib
from typing import Any, Dict
from dotenv import load_dotenv

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import django
from django.conf import settings
from django.utils.translation import gettext as _

# for run from ./bot/bot.py:
# import sys
# project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if project_path not in sys.path:
#     sys.path.append(project_path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async


# async def update_or_create_user(telegram_id, defaults):
#     User = get_user_model()
#     user, created = await User.objects.aupdate_or_create(telegram_id=telegram_id, defaults=defaults)
#     return user, created


async def create_user(telegram_id, defaults):
    User = get_user_model()
    user, created = await User.objects.aget_or_create(telegram_id=telegram_id, defaults=defaults)
    return user, created


@sync_to_async
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # refresh.payload.update(
    #     {
    #         'user_id': user.id,
    #         'telegram_id': user.telegram_id,
    #         'telegram_username': user.telegram_username,
    #     }
    # )

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def add_get_params_to_url(url: str, user_data: Dict[str, Any]):
    query_string = urllib.parse.urlencode(user_data)
    return f"{url}?{query_string}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = update.effective_user

    print('*********** /start *****************')
    print(user_data)
    print('****************************')

    if user_data is None:
        raise ValueError(
            f'handler_decor is made for communication with user, current update has not any user: {update}'
        )

    user_info = {
        'username': f'{user_data.id}',
        'telegram_id': user_data.id,
        'telegram_language': user_data.language_code or 'en',
        'telegram_username': user_data.username[:64] if user_data.username else '',
        'first_name': user_data.first_name[:60] if user_data.first_name else '',
        'last_name': user_data.last_name[:60] if user_data.last_name else '',
        'is_bot': 'Yes' if user_data.is_bot else 'No',
        'raw_data': user_data.to_dict(),
    }

    # user, created = await update_or_create_user(telegram_id=user_data.id, defaults=user_info)
    user, created = await create_user(telegram_id=user_data.id, defaults=user_info)

    # if user_data.language_code in map(lambda x: x[0], settings.LANGUAGES):
    #     site_language = user_data.language_code
    # else:
    #     site_language = settings.LANGUAGE_CODE

    if user.telegram_language and (user.telegram_language in map(lambda x: x[0], settings.LANGUAGES)):
        site_language = user.telegram_language
    elif user_data.language_code and (user_data.language_code in map(lambda x: x[0], settings.LANGUAGES)):
        site_language = user_data.language_code
    else:
        site_language = settings.LANGUAGE_CODE

    url_params = {}

    if user:
        tokens = await get_tokens_for_user(user)
        url_params['refresh'] = tokens['refresh']
        url_params['access'] = tokens['access']

    print('********* url_params ***********')
    print(url_params)
    print('**************************')

    open_map_text_en = 'Open Map'
    open_map_text_ru = 'Открыть Карту'
    open_map_text_uk = 'Відкрийте карту'

    open_settings_text_en = 'Open Settings'
    open_settings_text_ru = 'Открыть Настройки'
    open_settings_text_uk = 'Відкрийте налаштування'

    message_text_en = (
        "♥️ Hello! I am a demo application for <b>localization on a map</b> of places with <b>garbage</b>."
        + "\n\nYour language code: <b>en</b>"
    )

    message_text_ru = (
        "♥️ Приветствую! Я демо-приложение для <b>локализации на карте</b> мест с <b>мусором</b>."
        + "\n\nКод Вашего языка: <b>ru</b>"
    )

    message_text_uk = (
        "♥️ Вітаю! Я демонстраційний додаток для <b>локалізації на карті</b> місць зі <b>сміттям</b>."
        + "\n\nКод Вашої мови: <b>uk</b>"
    )

    message_text_another_language = (
        "♥️ Hello! I am a demo application for <b>localization on a map</b> of places with <b>garbage</b>."
        + f"\n\nYour language code: <b>{user_data.language_code}</b>"
    )

    if user_data.language_code == 'en':
        open_map_text = open_map_text_en
        open_settings_text = open_settings_text_en
        message_text = message_text_en

    elif user_data.language_code == 'ru':
        open_map_text = open_map_text_ru
        open_settings_text = open_settings_text_ru
        message_text = message_text_ru

    elif user_data.language_code == 'uk':
        open_map_text = open_map_text_uk
        open_settings_text = open_settings_text_uk
        message_text = message_text_uk

    else:
        open_map_text = open_map_text_en
        open_settings_text = open_settings_text_en
        message_text = message_text_another_language

    site_domain = 'https://ab73-91-211-135-87.ngrok-free.app'

    reply_markup = ReplyKeyboardMarkup.from_column(
        [
            KeyboardButton(
                text=open_map_text,
                web_app=WebAppInfo(
                    url=add_get_params_to_url(
                        # site_domain, url_params
                        f'{site_domain}/{site_language}/', url_params
                        # f"https://3649-91-211-135-87.ngrok-free.app/{site_language}/", user_info
                    )
                ),
            ),

            KeyboardButton(
                text=open_settings_text,
                web_app=WebAppInfo(
                    url=add_get_params_to_url(
                        f'{site_domain}/{site_language}/account/user/settings/', url_params
                    )
                ),
            ),
        ]
    )

    await update.effective_message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    text = f"🥲 Some error happened...\n" f"<b>Error:</b> {error}"
    await update.effective_message.reply_text(text=text, parse_mode=ParseMode.HTML)
    raise error


def run_bot(bot_token: str) -> None:
    application = (
        ApplicationBuilder()
        .token(bot_token)
        .concurrent_updates(True)
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .build()
    )

    # /start handler
    application.add_handler(CommandHandler("start", start))

    # error handler
    application.add_error_handler(error_handler)

    # start the bot
    print("Starting the bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(env_path)

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    print('****** bot_token: ', bot_token)
    if not bot_token:
        raise ValueError("Invalid TELEGRAM_BOT_TOKEN in .env file")

    run_bot(bot_token=bot_token)
