import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CONSULTANT_ID_STR = os.getenv("CONSULTANT_ID")
CONSULTANT_ID = int(CONSULTANT_ID_STR)

CHANNELS = ['@aiimpact_ir', '@ai_agent_farsi']
MESSAGE_LIMIT = 2

LIMIT_REACHED_MESSAGE = (
    "⚠️ شما به حداکثر پیام‌های رایگان خود در این ماه رسیده‌اید.\n\n"
    "برای دریافت مشاوره بیشتر(مشاوره تحصیلی و انتخاب رشته)، لطفاً با شماره‌های زیر تماس بگیرید:\n"
    "📞 <b>021-88785701</b>\n"
    "📱 <b>0903-4309895</b>\n"
    "یا اینکه فرم زیر را پر کنید تا با شما تماس بگیریم\n"
    "https://ostadbist.ir/contact/"
)