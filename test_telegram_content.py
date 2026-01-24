#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Telegram content formatting
"""

import os
from dotenv import load_dotenv
load_dotenv()

from channels.telegram.publisher import TelegramPublisher

def test_telegram_content():
    """Test what content is actually sent to Telegram."""
    
    print("🧪 Testing Telegram Content Formatting")
    print("=" * 40)
    
    # Test content
    test_title = "🔍 Скрытые риски в данных партнёра"
    test_description = "Компания выглядит надёжной, но скрывает долги и судебные разбирательства.\n\n🎯 Запишитесь на демо наших возможностей"
    full_content = f"{test_title}\n\n{test_description}"
    
    print("ОТПРАВЛЯЕМЫЙ ТЕКСТ:")
    print(repr(full_content))
    print()
    print("КАК ЭТО ВЫГЛЯДИТ:")
    print(full_content)
    print()
    
    try:
        publisher = TelegramPublisher()
        print("📤 Publishing test content...")
        success = publisher.publish_post(full_content)
        
        if success:
            print("✅ Test publication sent successfully!")
        else:
            print("❌ Test publication failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_telegram_content()