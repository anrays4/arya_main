import telebot
import requests
import json
import os # برای مدیریت متغیرهای محیطی

# --- تنظیمات ---
# توکن ربات تلگرام خود را اینجا قرار دهید
# بهتر است توکن را به عنوان یک متغیر محیطی (Environment Variable) تنظیم کنید
# مثال: TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = "7360480463:AAFqtRdIH6TX_c5gQPz224i31Fk91owmvHc" # توکن خود را اینجا بگذارید

# آدرس API چت‌بات شما
# مثال: CHATBOT_API_URL = "https://api.openai.com/v1/chat/completions"
# اگر از یک سرویس دیگر استفاده می‌کنید، URL مربوط به آن را قرار دهید.
CHATBOT_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" # URL API چت‌بات خود را اینجا بگذارید

# کلید API برای چت‌بات (اگر لازم است)
# مثال: CHATBOT_API_KEY = os.environ.get("OPENAI_API_KEY")
CHATBOT_API_KEY = "AIzaSyBW7HpJIqY0fQXCYrDAeDO_g6AJPWRFu7s" # کلید API چت‌بات خود را اینجا بگذارید

# --- راه‌اندازی ربات تلگرام ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# --- تابع برای ارتباط با API چت‌بات ---
def get_chatbot_response(user_message):
    headers = {
        "Content-Type": "application/json",
        # اگر API چت‌بات شما به کلید احراز هویت در هدر نیاز دارد، آن را اضافه کنید
        # مثال برای OpenAI:
        # "Authorization": f"Bearer {CHATBOT_API_KEY}"
    }

    # ساختار درخواست برای API چت‌بات ممکن است متفاوت باشد
    # این یک مثال عمومی است.
    payload = {
        # مثال برای OpenAI (مدل gpt-3.5-turbo):
        # "model": "gpt-3.5-turbo",
        # "messages": [
        #     {"role": "system", "content": "You are a helpful assistant specialized in Iranian law."},
        #     {"role": "user", "content": user_message}
        # ]
        # اگر از یک API ساده‌تر استفاده می‌کنید:
        "query": user_message,
        "context": "پاسخ‌ها باید در مورد حقوق و قوانین ایران باشند."
    }

    try:
        response = requests.post(CHATBOT_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # برای بررسی خطاهای HTTP
        response_data = response.json()

        # استخراج پاسخ از ساختار JSON API چت‌بات
        # این بخش باید بر اساس ساختار پاسخ API چت‌بات شما تغییر کند.
        # مثال برای OpenAI:
        # if response_data and "choices" in response_data and len(response_data["choices"]) > 0:
        #     return response_data["choices"][0]["message"]["content"]
        # مثال برای یک API ساده‌تر که "answer" را برمی‌گرداند:
        if "answer" in response_data:
            return response_data["answer"]
        elif "response" in response_data: # یا اگر فیلد پاسخ "response" نام دارد
            return response_data["response"]
        else:
            return "متاسفانه نتوانستم پاسخ مناسبی از چت‌بات دریافت کنم."

    except requests.exceptions.RequestException as e:
        print(f"خطا در ارتباط با API چت‌بات: {e}")
        return "متاسفانه در حال حاضر امکان ارتباط با سرویس چت‌بات وجود ندارد. لطفا بعدا تلاش کنید."
    except json.JSONDecodeError:
        print(f"خطا در دیکد کردن پاسخ JSON از API چت‌بات: {response.text}")
        return "پاسخ نامعتبری از چت‌بات دریافت شد."
    except Exception as e:
        print(f"خطای ناشناخته: {e}")
        return "مشکلی پیش آمده است. لطفا دوباره تلاش کنید."

# --- هندلر برای دستور /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من ربات حقوقی ایران هستم. سوالات خود را در مورد حقوق ایران بپرسید.")

# --- هندلر برای تمام پیام‌های متنی ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_question = message.text
    bot.send_chat_action(message.chat.id, 'typing') # نمایش "در حال تایپ..."
    chatbot_answer = get_chatbot_response(user_question)
    bot.reply_to(message, chatbot_answer)

# --- شروع به گوش دادن برای پیام‌ها ---
print("ربات در حال اجرا است...")
bot.polling(non_stop=True)