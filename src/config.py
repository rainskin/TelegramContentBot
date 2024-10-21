from core.env import env

BOT_TOKEN = env.get('BOT_TOKEN')

MONGO_URL = env.get('MONGO_URL')
MONGO_DB_NAME = env.get('MONGO_DB_NAME')

API_ID = env.get_int('API_ID')
API_HASH = env.get('API_HASH')

UPLOAD_CHANNEL_LINK = env.get('UPLOAD_CHANNEL_LINK')
UPLOAD_CHANNEL_ID = env.get_int('UPLOAD_CHANNEL_ID')

USERBOT_SESSION_STRING = env.get('USERBOT_SESSION_STRING')

