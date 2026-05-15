# ✈️ Telegram Bot & Channel Setup Guide

To automate posts to your Telegram Channel, follow these steps to get your **Bot Token** and **Channel ID**.

### 1. Create a Bot with BotFather
1. Open Telegram and search for [@BotFather](https://t.me/botfather).
2. Type `/newbot` and follow the prompts (give it a name like "Autoflock Bot").
3. **BotFather** will give you an **API Token** (e.g., `123456789:ABCdefGHI...`).
4. **Copy this Token.**

### 2. Set Up Your Channel
1. Create a new **Telegram Channel** (Public or Private).
2. Add your new bot as an **Administrator** of the channel.
3. Make sure the bot has the "Post Messages" permission.

### 3. Get Your Channel ID
The easiest way to get the ID:
1. Send a test message to your channel.
2. Forward that message to [@userinfobot](https://t.me/userinfobot) or [@JsonDumpBot](https://t.me/jsondumpbot).
3. It will reply with a number. 
   - **Public Channels**: You can also use the username (e.g., `@my_ai_channel`).
   - **Private Channels**: The ID usually looks like `-1001234567890`.

### 4. Update Autoflock
Paste these values into `/data/data/com.termux/files/home/projects/media/autoflock/config/social.json`:
```json
{
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_channel_id": "YOUR_CHANNEL_ID"
}
```
