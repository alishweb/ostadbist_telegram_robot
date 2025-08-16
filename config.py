import os

API_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
CONSULTANT_ID = int(os.getenv("CONSULTANT_ID", "43434343"))
CHANNELS = ['@aiimpact_ir', '@ai_agent_farsi']

DB_FILE = "consultant_bot.db"
MESSAGE_LIMIT = 2
