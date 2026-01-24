#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Instagram Account Search
Тестування пошуку акаунтів в Instagram за ключовими словами
"""

import os
import asyncio
from dotenv import load_dotenv
from channels.instagram.collector import InstagramCollector

load_dotenv()

def test_account_search():
    """Тест пошуку акаунтів в Instagram"""
    print("🔍 Testing Instagram Account Search")
    print("=" * 40)

    try:
        collector = InstagramCollector()

        # Ключові слова для пошуку акаунтів по темі будівництва/ремонту
        keywords = [
            'Bau',           # Будівництво (німецька)
            'Renovierung',   # Ремонт (німецька)
            'Immobilien',    # Нерухомість (німецька)
            'Handwerker',    # Ремісник
            'Baufirma',      # Будівельна компанія
            'Sanierung',     # Санування
            'Architekt',     # Архітектор
            'Baumarkt',      # Будівельний ринок
            'Innenausbau',   # Внутрішнє оздоблення
        ]

        print(f"📋 Searching for Instagram accounts with keywords: {keywords}")
        print("   This may take a few minutes...")

        accounts = collector.search_accounts(keywords, limit=10)

        print(f"\n✅ Found {len(accounts)} accounts:")
        print("-" * 80)

        for i, account in enumerate(accounts, 1):
            print(f"{i:2d}. @{account['username']}")
            print(f"    Name: {account['full_name']}")
            print(f"    Followers: {account['follower_count']:,}")
            print(f"    Following: {account['following_count']:,}")
            print(f"    Business: {'Yes' if account['is_business'] else 'No'}")
            print(f"    Verified: {'Yes' if account['is_verified'] else 'No'}")
            print(f"    Bio: {account['bio'][:100]}{'...' if len(account['bio']) > 100 else ''}")
            print(f"    Found via: {account['search_keyword']}")
            print()

        if accounts:
            print("💡 Next steps:")
            print("   1. Analyze followers of these accounts for B2B leads")
            print("   2. Use collect_from_found_accounts() to get detailed follower data")
            print("   3. Score leads using InstagramAnalyzer")
            print("   4. Send targeted invitations")
        else:
            print("❌ No accounts found. Try different keywords or check Instagram credentials.")

    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("   Make sure your Instagram credentials are correct and you have internet connection.")
        print("   Note: Instagram may block automated searches - try manual search first.")

if __name__ == "__main__":
    test_account_search()