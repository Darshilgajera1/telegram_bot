import json
import os
from urllib.parse import quote_plus

import requests as requests
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
from telegram.utils.request import Request

from constants import START_COMMAND, EXIST_TOKEN, PUSH_USER_DATA, GET_ALL_USER, ALL_TOKEN_QUERY, DELETE_ONE_TOKEN, \
    DELETE_DATA_QUERY, LIST_QUERY
from db_connection import db

load_dotenv()


TELEGRAM_ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN')
access_token_secret = os.getenv('TELEGRAM_TOKEN_SECRET')
BOT_TOKEN = os.getenv('BOT_TOKEN')


def set_my_commands():
    bot_commands = [{"command": "start", "description": "Starting bot"},
                    {"command": "stop", "description": "stop bot"},
                    {"command": "list", "description": "List all the tokens"},
                    {"command": "remove", "description": "To remove the token"}]
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/setMyCommands?commands=' + str(json.dumps(bot_commands))
    response = requests.get(send_text)


def message_handler(update, context):
    user_messages = update.message.text

    if user_messages.lower() == "/start":
        set_my_commands()
        update.message.reply_text(START_COMMAND)

    elif len(user_messages) == 42:
        if len(user_messages) == 42:
            db_token_id = user_messages
            db_chat_id = update.message.chat_id
            exist_token = db.fetchall(EXIST_TOKEN.format(db_token_id=db_token_id, db_chat_id=db_chat_id))
            if exist_token:
                update.message.reply_text(f"You already configure this Token {db_token_id}")
            else:
                user_data_query = db.fetchall(PUSH_USER_DATA.format(db_token_id=db_token_id, chat_id=db_chat_id))
                update.message.reply_text(f"Thanks! Now you configured all the tweets of this {db_token_id}")
        else:
            update.message.reply_text("Sorry, this token id is not valid")

    elif user_messages == "/tweets":
        get_messages = {'MessageId': '3b272fda-03f0-4d53-8736-c6651643f7c1',
                        'ReceiptHandle': 'AQEB9aTqvAyKW38SUn6adPx30hNrilL54vLlSGbhhbgY6/muhBlp49lkN+4QyHfD6vjntoLzg1QU+i5fZ2nGz0bJKisufPHFeVNLhB9psx/N3YMT549yMQq0uFuCruH4Zqp0dryr0FFoWv+AxY0PA7wl4Jgp2Zd2/0hbS6RpULjbDyGQOTfe7SzrIjJIqzWBwTa36j0m8DXvXg+O3ZNI7OUt9BRhB/ZzlNI+E+rLPvpZ5zR1sQzDJdL+aFcfzeKCwVCjOKAQzwjkUn9L4NWVVGhFtj8t/pTIt9IICIXqp/UVzjIWnsZyNEzLdbTLy1ODnbf3',
                        'MD5OfBody': '11e8cd598ccf2fad3d037764d188a770',
                        'Body': 'Build During The Bear &amp; Thrive During The Bull. Congrats To @DecentraBnB @MajesticDrama On Their #CMC Listing! $DBNB https://t.co/N5g7Jax0ia',
                        'Attributes': {'SenderId': 'AROAZ5WY3GSXJBSKHKAEK:record_relevant_tweets',
                                       'ApproximateFirstReceiveTimestamp': '1660423153776',
                                       'ApproximateReceiveCount': '1',
                                       'SentTimestamp': '1660422607924', 'SequenceNumber': '18871812261338095872',
                                       'MessageDeduplicationId': 'tts_1660422607', 'MessageGroupId': 'tts__1660422607'},
                        'MD5OfMessageAttributes': 'f96937c17ab64086c274e455ba0fd752', 'MessageAttributes': {
                'matching_pairs': {
                    'StringValue': "[{'pair_id': '0x1e969a1b1983e383aa3a261f7da055e1b403bbcd', 'token_id': '0x833850be8858722cfc5e5e75f2fe6275e055d888', 'name': 'DecentraBNB', 'symbol': 'DBNB'}]",
                    'DataType': 'String'}}}
        list_token_id = []
        msg_body = get_messages['Body']
        get_msg = get_messages['MessageAttributes']['matching_pairs']
        dd = get_msg['StringValue']
        res = list(eval(dd))
        for i in res:
            list_token_id.append(i['token_id'])
        for i in list_token_id:
            user_chat_id = db.fetchall(GET_ALL_USER.format(db_token_id=i))
            for each_chat in user_chat_id:
                each_chat_id = each_chat[0]
                send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + each_chat_id + '&parse_mode=Markdown&text=' + quote_plus(msg_body)
                response = requests.get(send_text)

    elif user_messages.lower() == "/remove" or user_messages.startswith('/remove_'):
        if user_messages.lower() == "/remove":
            chat_id = update.message.chat_id
            token_query = db.fetchall(ALL_TOKEN_QUERY.format(chat_id=chat_id))
            if token_query:
                str = ''
                for item in token_query:
                    str += item[0] + ','
                update.message.reply_text(
                    f"What token do you want remove {str}.\n You can remove with /remove + _token_id where token id is equal to your id")
            else:
                update.message.reply_text(f"You dont configured any token id you can start with /start")
        else:
            data = user_messages.split('_')
            db_token_id = data[1]
            db_chat_id = update.message.chat_id
            delete_one_token = db.fetchall(DELETE_ONE_TOKEN.format(db_token_id=db_token_id, db_chat_id=db_chat_id))
            update.message.reply_text(f"Token id {db_token_id} is now unconfigured. \n Thanks")

    elif user_messages.lower() == "/stop":
        chat_id = update.message.chat_id
        delete_query = db.fetchall(DELETE_DATA_QUERY.format(chat_id=chat_id))

    elif user_messages.lower() == '/list':
        chat_id = update.message.chat_id
        list_query = db.fetchall(LIST_QUERY.format(chat_id=chat_id))
        print('===', list_query)
        str = ''
        for item in list_query:
            print(item)
            str += item[0] + ','
        update.message.reply_text(f"All the list\n {str} You can remove with /remove")


def main():
    telegram_request = Request(connect_timeout=0.5)
    telegram_bot = Bot(request=telegram_request, token=os.getenv('BOT_TOKEN'))
    updater = Updater(bot=telegram_bot, use_context=True)
    telegram_dispatcher = updater.dispatcher
    telegram_dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    # this updater.start_polling(6) used for checking message every 6 seconds
    updater.start_polling(timeout=123)
    updater.idle()

main()