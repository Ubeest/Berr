import os
import zipfile
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# تعيين توكن البوت الخاص بك هنا
TOKEN = "6997077673:AAGJlmkamcTEzUG8jVnA21fekxjg1GGcrJ4"

# قائمة بأيدي المطورين
DEVELOPERS = [5150924482, 5150924482]  # قم بتغيير الأرقام بأيدي المطورين الخاصة بك

# تعيين مسار للمجلد الذي يحتوي على الملفات المضغوطة
ZIP_FOLDER = "zipped_files"

# إنشاء المجلد إذا لم يكن موجودًا
os.makedirs(ZIP_FOLDER, exist_ok=True)

# معالج الأمر /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the File Zipper Bot!")

# معالج الأمر /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me the URL of the website you want to zip its files.")

# معالج الرسائل
def handle_message(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id in DEVELOPERS:
        # إذا كان المرسل للرسالة مطورًا
        url = update.message.text
        try:
            # تحميل صفحة الويب
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # جمع الروابط
            links = [link.get('href') for link in soup.find_all('a', href=True)]
            # تنزيل وضغط الملفات
            with zipfile.ZipFile(os.path.join(ZIP_FOLDER, "zipped_files.zip"), "w") as zip_ref:
                for link in links:
                    try:
                        # تنزيل الملفات
                        file_response = requests.get(link)
                        # حفظ الملفات في مجلد مؤقت
                        with open(os.path.join(ZIP_FOLDER, os.path.basename(link)), "wb") as f:
                            f.write(file_response.content)
                        # إضافة الملفات إلى ملف zip
                        zip_ref.write(os.path.join(ZIP_FOLDER, os.path.basename(link)))
                    except Exception as e:
                        print(f"Error downloading file {link}: {e}")
            # إرسال ملف zip إلى المستخدم
            context.bot.send_document(update.effective_chat.id, open(os.path.join(ZIP_FOLDER, "zipped_files.zip"), "rb"))
        except Exception as e:
            update.message.reply_text("An error occurred: {}".format(str(e)))
    else:
        update.message.reply_text("You are not authorized to use this bot.")

def main() -> None:
    # إنشاء البوت وتعيين المعالجات
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
