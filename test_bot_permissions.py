#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Telegram bot permissions
"""

import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from telegram import Bot
from telegram.error import TelegramError

async def test_bot_permissions():
    """Test if bot can access the channel."""
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    print("🔍 Testing Telegram Bot Permissions")
    print("=" * 40)
    print(f"Channel ID: {channel_id}")
    
    bot = Bot(token=bot_token)
    
    try:
        # Test getting chat info
        print("📡 Getting chat info...")
        chat = await bot.get_chat(chat_id=channel_id)
        print(f"✅ Chat found: {chat.title}")
        print(f"   Type: {chat.type}")
        print(f"   Username: {chat.username}")
        
        # Test sending a message
        print("📤 Testing message send...")
        message = await bot.send_message(
            chat_id=channel_id,
            text="🔧 Тест подключения бота к каналу"
        )
        print(f"✅ Test message sent successfully!")
        print(f"   Message ID: {message.message_id}")
        
    except TelegramError as e:
        print(f"❌ Telegram Error: {e}")
        if "chat not found" in str(e).lower():
            print("💡 Возможные причины:")
            print("   - Бот не добавлен в канал")
            print("   - Неправильный CHANNEL_ID")
            print("   - Канал приватный и бот не имеет доступа")
        elif "not enough rights" in str(e).lower():
            print("💡 Бот добавлен в канал, но не имеет прав на публикацию")
            print("   - Сделайте бота администратором канала")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot_permissions())