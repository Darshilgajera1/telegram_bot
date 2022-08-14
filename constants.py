START_COMMAND = "Hey! Welcome to innit bot. Innitbot helps you to track all the tweets that you want. Enter Your Token ID to go further!"
EXIST_TOKEN = """SELECT token_id,telegram_chat_id FROM innit_dump.telegram_user_token WHERE telegram_chat_id = '{db_chat_id}' AND token_id = '{db_token_id}'"""
PUSH_USER_DATA = """INSERT INTO innit_dump.telegram_user_token (telegram_chat_id,token_id) VALUES ('{chat_id}','{db_token_id}')"""
GET_ALL_USER = """SELECT telegram_chat_id from innit_dump.telegram_user_token WHERE token_id='{db_token_id}'"""
ALL_TOKEN_QUERY = """SELECT token_id FROM innit_dump.telegram_user_token where telegram_chat_id = '{chat_id}'"""
DELETE_ONE_TOKEN = """DELETE FROM innit_dump.telegram_user_token WHERE telegram_chat_id = '{db_chat_id}' AND token_id = '{db_token_id}'"""
DELETE_DATA_QUERY = """DELETE FROM innit_dump.telegram_user_token WHERE telegram_chat_id = '{chat_id}'"""
LIST_QUERY = """SELECT token_id FROM innit_dump.telegram_user_token WHERE telegram_chat_id = '{chat_id}'"""




















GET_UNISWAP_PAIR_DATA_QUERY = "SELECT pair_id, symbol, base_token_symbol, name, base_token_name, token_id, latest_liquidity, total_supply, latest_market_cap, liquidity_lock_percentage " \
                              "FROM innit_dump.uniswap_v2_pairs WHERE token_id = '{token_id}';"


GET_INFUENCER_TWEETS_QUERY = """
SELECT et.tweet_id, et.author_id, et.body, et.author_handle, et.tweet_create_time, et.retweet_count, et.like_count, et.reply_count, et.quote_count, et.profile_image_url 
FROM innit_dump.enhanced_tweets et 
JOIN innit_dump.tweet_token_map ttm 
ON ttm.tweet_id = et.tweet_id 
WHERE ttm.token_id = '{token_id}' AND et.tweet_create_time > '{date}'"""
