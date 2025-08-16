from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from html import escape
import aiosqlite
import datetime
import re

# چون از این موارد در فایل questions.py هم استفاده می‌شود، اینجا تعریف می‌کنیم
from db import get_or_create_user, update_user_details
from middlewares import check_subscription, get_join_channels_keyboard
from config import MESSAGE_LIMIT, LIMIT_REACHED_MESSAGE

# تعریف State ها در یک مکان مرکزی
class Consultation(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_phone_number = State()
    waiting_for_grade = State()
    waiting_for_question = State()

router = Router()

def get_ask_new_question_keyboard():
    buttons = [[InlineKeyboardButton(text="❓ پرسیدن سوال جدید", callback_data="ask_new_question")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, db: aiosqlite.Connection):
    if not await check_subscription(message.bot, message.from_user.id):
        await message.answer("⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های زیر عضو شوید:", reply_markup=get_join_channels_keyboard())
        return

    user_data = await get_or_create_user(db, message.from_user.id)
    if user_data[0]:  # اگر کاربر قبلاً ثبت‌نام کرده
        current_month = datetime.datetime.now().month
        is_new_month = user_data[4] != current_month
        effective_count = 0 if is_new_month else user_data[3]
        
        if effective_count >= MESSAGE_LIMIT:
            await message.answer(LIMIT_REACHED_MESSAGE)
            return
        
        await message.answer(f"سلام {escape(user_data[0])} عزیز، خوش برگشتید! 👋", reply_markup=get_ask_new_question_keyboard())
    else: # اگر کاربر جدید است
        await message.answer("سلام! به ربات مشاوره خوش آمدید. 👋\n\nلطفاً نام و نام خانوادگی خود را ارسال کنید:")
        await state.set_state(Consultation.waiting_for_full_name)

@router.callback_query(F.data == "check_join")
async def check_join_callback(callback: CallbackQuery, state: FSMContext, db: aiosqlite.Connection):
    await callback.answer("در حال بررسی عضویت شما...", show_alert=False)
    if await check_subscription(callback.bot, callback.from_user.id):
        await callback.message.delete()
        user_data = await get_or_create_user(db, callback.from_user.id)
        if user_data[0]:
            await callback.message.answer(f"سلام {escape(user_data[0])} عزیز! عضویت شما تایید شد.✅", reply_markup=get_ask_new_question_keyboard())
        else:
            await callback.message.answer("عالی! عضویت شما تایید شد. ✅\n\nلطفاً نام و نام خانوادگی خود را ارسال کنید:")
            await state.set_state(Consultation.waiting_for_full_name)
    else:
        await callback.answer("❌ شما هنوز در تمام کانال‌ها عضو نشده‌اید.", show_alert=True)
        await callback.message.answer("⚠️ **بررسی ناموفق بود!**\n\nهنوز عضو تمام کانال‌ها نشده‌اید. لطفاً مجدداً تلاش کنید.")

@router.message(Consultation.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    # Regex برای بررسی حروف فارسی/انگلیسی و فاصله، با طول بین ۳ تا ۵۰ کاراکتر
    name_pattern = r"^[\u0600-\u06FF\sA-Za-z]{3,50}$"
    
    if re.match(name_pattern, message.text) and ' ' in message.text:
        await state.update_data(full_name=message.text)
        await message.answer("متشکرم. اکنون لطفاً شماره تماس خود را ارسال کنید:")
        await state.set_state(Consultation.waiting_for_phone_number)
    else:
        await message.answer("❌ نام وارد شده نامعتبر است.\n\n"
                             "لطفاً نام و نام خانوادگی خود را به درستی (شامل حروف و یک فاصله) وارد کنید.")
        return
    


def get_grade_keyboard():
    buttons = [
        [KeyboardButton(text="دهم"), KeyboardButton(text="یازدهم"), KeyboardButton(text="دوازدهم")],
        [KeyboardButton(text="فارغ‌التحصیل"), KeyboardButton(text="سایر مقاطع")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


@router.message(Consultation.waiting_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    phone_pattern = r"^09\d{9}$"
    if re.match(phone_pattern, message.text):
        await state.update_data(phone_number=message.text)
        await message.answer(
            "بسیار خب. حالا لطفاً پایه تحصیلی خود را از گزینه‌های زیر انتخاب کنید:",
            reply_markup=get_grade_keyboard()
        )
        await state.set_state(Consultation.waiting_for_grade)
    else:
        await message.answer("❌ شماره تلفن وارد شده نامعتبر است.\n\n"
                             "لطفاً شماره خود را به فرمت صحیح وارد کنید (مثلاً: 09123456789).")
        return

VALID_GRADES = ["دهم", "یازدهم", "دوازدهم", "فارغ‌التحصیل", "سایر مقاطع"]

@router.message(Consultation.waiting_for_grade, F.text.in_(VALID_GRADES))
async def process_grade(message: Message, state: FSMContext, db: aiosqlite.Connection):
    await state.update_data(grade=message.text)
    data = await state.get_data()
    await update_user_details(db, message.from_user.id, data['full_name'], data['phone_number'], data['grade'])
    
    await message.answer(
        "اطلاعات شما با موفقیت ذخیره شد. ✅\nاکنون می‌توانید سوال خود را تایپ و ارسال کنید.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Consultation.waiting_for_question)

@router.message(Consultation.waiting_for_grade)
async def process_grade_invalid(message: Message):
    """مواقعی را مدیریت می‌کند که کاربر به جای استفاده از کیبورد، چیزی تایپ می‌کند."""
    await message.answer("❌ لطفاً فقط یکی از گزینه‌های روی کیبورد را انتخاب کنید.")