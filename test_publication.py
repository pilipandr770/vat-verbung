#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Publication Script
Тестирование публикации контента в Telegram локально
"""

import logging
import os
from dotenv import load_dotenv
from core.content_engine import ContentEngine
from channels.telegram.publisher import TelegramPublisher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

def test_telegram_publication():
    """Test publishing content to Telegram"""
    logger.info("🚀 Starting Telegram Publication Test")

    try:
        # Initialize components
        logger.info("📦 Initializing Content Engine...")
        content_engine = ContentEngine()

        logger.info("📱 Initializing Telegram Publisher...")
        telegram_publisher = TelegramPublisher()

        # Generate content
        logger.info("🎨 Generating content...")
        content, topic, content_type = content_engine.generate_content()
        logger.info(f"✅ Generated: {topic.value}/{content_type.value}")
        logger.info(f"📝 Content: {content[:100]}...")

        # Test publication
        logger.info("📤 Publishing to Telegram...")
        success = telegram_publisher.publish_post(content)

        if success:
            logger.info("✅ Publication successful!")
            return True
        else:
            logger.error("❌ Publication failed!")
            return False

    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        return False

def test_content_generation():
    """Test content generation only"""
    logger.info("🎨 Testing Content Generation...")

    try:
        content_engine = ContentEngine()

        # Generate multiple samples
        for i in range(3):
            content, topic, content_type = content_engine.generate_content()
            logger.info(f"📝 Sample {i+1}: {topic.value}/{content_type.value}")
            logger.info(f"   {content[:150]}...")
            logger.info("")

        logger.info("✅ Content generation working!")
        return True

    except Exception as e:
        logger.error(f"❌ Content generation failed: {e}", exc_info=True)
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 PROMOTION HUB - LOCAL PUBLICATION TEST")
    print("=" * 60)

    # Test 1: Content Generation
    print("\n1️⃣ Testing Content Generation...")
    content_ok = test_content_generation()

    if not content_ok:
        print("❌ Content generation failed. Stopping tests.")
        return 1

    # Test 2: Telegram Publication
    print("\n2️⃣ Testing Telegram Publication...")
    print("⚠️  This will actually post to your Telegram channel!")
    response = input("Continue with publication test? (y/N): ").lower().strip()

    if response == 'y':
        publish_ok = test_telegram_publication()
        if publish_ok:
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Publication test failed!")
            return 1
    else:
        print("⏭️  Skipping publication test.")
        print("✅ Content generation test passed!")
        return 0

if __name__ == "__main__":
    exit(main())