#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check recent messages in Telegram channel
"""

import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from telegram import Bot

async def check_recent_messages():
    """Check recent messages in the channel."""
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    print("📋 Checking Channel Status")
    print("=" * 40)
    
    bot = Bot(token=bot_token)
    
    try:
        # Get chat info
        print("📡 Getting chat info...")
        chat = await bot.get_chat(chat_id=channel_id)
        print(f"✅ Channel: {chat.title}")
        print(f"   Type: {chat.type}")
        print(f"   Members: {getattr(chat, 'members_count', 'N/A')}")
        print(f"   Username: {chat.username}")
        print(f"   Description: {chat.description[:100] if chat.description else 'No description'}...")
        
        # Try to get message count (approximate)
        print()
        print("💡 To see messages, open the channel in Telegram Web:")
        print(f"   https://web.telegram.org/a/#{chat.username}")
        print()
        print("🔍 Recent test messages should appear there")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_recent_messages())