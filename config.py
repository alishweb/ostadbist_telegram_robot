import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CONSULTANT_IDS_STR = os.getenv("CONSULTANT_IDS", "")
if not CONSULTANT_IDS_STR:
    raise ValueError("حداقل یک آیدی مشاور در فایل .env در متغیر CONSULTANT_IDS نیاز است.")
CONSULTANT_IDS = [int(cid.strip()) for cid in CONSULTANT_IDS_STR.split(',')]
OWNER_ID = int(os.getenv("OWNER_ID"))

CHANNELS = ['@toofanito', '@konkoor_toofan']
MESSAGE_LIMIT = 2

LIMIT_REACHED_MESSAGE = (
    "⚠️ شما به حداکثر پیام‌های رایگان خود در این ماه رسیده‌اید.\n\n"
    "برای دریافت مشاوره بیشتر(مشاوره تحصیلی و انتخاب رشته)، لطفاً با شماره‌های زیر تماس بگیرید:\n"
    "📞 <b>02188785701</b>\n"
    "📱 <b>09026046184</b>\n"
    "همچنین می‌توانید از طریق لینک زیر اطلاعات بیشتری درباره انتخاب رشته کسب کنید: \n"
    "https://ostadbist.ir/entekhab-reshte"
    "یا اینکه فرم زیر را پر کنید تا با شما تماس بگیریم\n"
    "https://ostadbist.ir/contact/ \n"
)