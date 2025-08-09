# Shellgram

> ⚠️ Educational use only! This project is a proof-of-concept and should not be used for malicious purposes.

## Disclaimer

**IMPORTANT:** This software is intended for educational and demonstration purposes only.

Use this Telegram bot **ONLY** on computers you own or have explicit permission to access.

The author of this project **does not take any responsibility** for any misuse, illegal activities, or damages caused by this software.

This project is provided "AS IS", without any warranties or guarantees of any kind, either express or implied.

By using this software, you agree that you are solely responsible for any consequences arising from its use.


## 📌 Features
- Run shell commands remotely via Telegram
- Upload & download files
- Take screenshots of the target machine
- Get detailed system information

## 🚀 Installation
```bash
git clone https://github.com/username/remote-admin-bot.git
cd remote-admin-bot
pip install -r requirements.txt
```

## ⚙️ Configuration
Create a .env file in the project root:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
AUTHORIZED_USER_ID=123456789
```

## ▶️ Usage
```bash
python bot.py
```

## 💻 Commands
| Command      | Description               |
| ------------ | ------------------------- |
| `/start`     | Show main menu            |
| `/shell` cmd | Execute shell command     |
| `/download`  | Download file from target |
| `/upload`    | Upload file to target     |
| `/sysinfo`   | Show system information   |

## 🖼 Screenshot Example
