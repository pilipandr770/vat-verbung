#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Telegram publication fix
"""

import os
from dotenv import load_dotenv
load_dotenv()

from channels.telegram.publisher import TelegramPublisher

def test_telegram_publication():
    """Test Telegram publication with async fix."""

    print("🧪 Testing Telegram Publication Fix")
    print("=" * 40)

    try:
        # Initialize publisher
        publisher = TelegramPublisher()
        print("✅ Telegram publisher initialized")

        # Test publication
        test_content = "🧪 Тест публикации в Telegram канал\n\nЭто тест исправления асинхронного кода."
        print(f"📤 Publishing test content: {test_content[:50]}...")

        success = publisher.publish_post(test_content)

        if success:
            print("✅ SUCCESS: Test publication sent to Telegram!")
        else:
            print("❌ FAILED: Test publication failed")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_telegram_publication()