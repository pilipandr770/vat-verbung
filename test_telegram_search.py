#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Telegram Group Search
Тестування пошуку груп в Telegram за ключовими словами
"""

import os
import asyncio
from dotenv import load_dotenv
from channels.telegram.collector import TelegramCollector

load_dotenv()

async def test_group_search():
    """Тест пошуку груп в Telegram"""
    print("🔍 Testing Telegram Group Search")
    print("=" * 40)

    collector = TelegramCollector()

    if not collector.api_id or not collector.api_hash:
        print("❌ TELEGRAM_API_ID or TELEGRAM_API_HASH not configured")
        print("   Get credentials from: https://my.telegram.org/auth")
        return

    # Ключові слова для пошуку груп по темі будівництва/ремонту
    keywords = [
        'Bau',           # Будівництво (німецька)
        'Renovierung',   # Ремонт (німецька)
        'Immobilien',    # Нерухомість (німецька)
        'Baufirma',      # Будівельна компанія
        'Handwerker',    # Ремісник
        'Sanierung'      # Санування
    ]

    print(f"📋 Searching for groups with keywords: {keywords}")
    print("   This may take a few minutes...")

    try:
        groups = await collector.search_groups(keywords, limit=20)

        print(f"\n✅ Found {len(groups)} groups:")
        print("-" * 60)

        for i, group in enumerate(groups, 1):
            print(f"{i:2d}. {group['title']}")
            print(f"    ID: {group['id']}")
            print(f"    Username: @{group.get('username', 'N/A')}")
            print(f"    Members: {group.get('participants_count', 'N/A')}")
            print(f"    Found via: {group['keyword']}")
            print()

        if groups:
            print("💡 To collect leads from these groups, add their IDs to your scheduler")
            print("   Example: chat_ids = [-1001234567890, -1009876543210]")
        else:
            print("❌ No groups found. Try different keywords or check API credentials.")

    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("   Make sure your API credentials are correct and you have internet connection.")

if __name__ == "__main__":
    asyncio.run(test_group_search())