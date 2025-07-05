import telebot
from transformers import pipeline

# التوكن الخاص بك
TOKEN = "7924896220:AAG7pto9wIj7Lab3hD6aUuCkB8DHXQSR8Dw"
bot = telebot.TeleBot(TOKEN)

# نموذج التلخيص
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحبًا بك في بوت التلخيص الذكي!\nأرسل نصًا وسأقوم بتلخيصه لك.\nيمكنك أيضًا استخدام الأمر /summary متبوعًا بعدد الجمل.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "📝 فقط أرسل أي نص طويل وسأقوم بتلخيصه لك.\nاستخدم الأمر /summary [عدد_الجمل] لاختيار حجم الملخص.")

@bot.message_handler(commands=['summary'])
def custom_summary(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗️يرجى تحديد عدد الجمل مثل: /summary 3")
            return
        sentence_count = int(args[1])
        msg = bot.reply_to(message, "📨 أرسل الآن النص المراد تلخيصه:")
        bot.register_next_step_handler(msg, lambda m: summarize_text(m, sentence_count))
    except:
        bot.reply_to(message, "❌ حدث خطأ. تأكد من استخدام الأمر بالشكل الصحيح.")

def summarize_text(message, sentence_count=3):
    try:
        summary = summarizer(message.text, max_length=sentence_count*20, min_length=sentence_count*10, do_sample=False)[0]['summary_text']
        bot.send_message(message.chat.id, f"📌 الملخص:\n\n{summary}")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ لم أتمكن من تلخيص النص. حاول مرة أخرى.")

@bot.message_handler(func=lambda message: True)
def default_summary(message):
    try:
        summary = summarizer(message.text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        bot.reply_to(message, f"📌 الملخص:\n\n{summary}")
    except Exception as e:
        bot.reply_to(message, "❌ لم أتمكن من تلخيص النص. تأكد من أنه ليس قصيرًا جدًا.")

bot.polling()