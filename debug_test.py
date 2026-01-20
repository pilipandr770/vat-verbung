#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug Script - Test AI Content Generation Locally
Тестирование AI генерации контента без других зависимостей
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ai_providers():
    """Test AI providers availability"""
    logger.info("=" * 60)
    logger.info("Testing AI Providers")
    logger.info("=" * 60)
    
    # Test OpenAI
    try:
        from core.ai_content import AIProvider
        provider = AIProvider()
        logger.info("✓ OpenAI Provider imported successfully")
        if provider.client:
            logger.info(f"  - Model: {provider.model}")
            logger.info(f"  - Status: READY")
        else:
            logger.warning("  - Status: API KEY NOT CONFIGURED")
    except Exception as e:
        logger.error(f"✗ OpenAI Provider error: {e}")
    
    # Test Gemini
    try:
        from core.ai_content import GeminiProvider
        provider = GeminiProvider()
        logger.info("✓ Gemini Provider imported successfully")
        if provider.client:
            logger.info(f"  - Model: {provider.model}")
            logger.info(f"  - Status: READY")
        else:
            logger.warning("  - Status: API KEY NOT CONFIGURED")
    except Exception as e:
        logger.error(f"✗ Gemini Provider error: {e}")

def test_content_engine():
    """Test content engine"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Content Engine")
    logger.info("=" * 60)
    
    try:
        from core.content_engine import ContentEngine, ContentTopic, ContentType
        engine = ContentEngine()
        logger.info("✓ Content Engine initialized")
        
        # Test generating content
        logger.info("\nGenerating sample content...")
        for topic in [ContentTopic.AUTOMATION, ContentTopic.RISKS]:
            for ctype in [ContentType.PAIN]:
                logger.info(f"\n  Testing {topic.value}/{ctype.value}...")
                content, returned_topic, returned_type = engine.generate_content(
                    topic=topic,
                    content_type=ctype,
                    use_ai=True
                )
                if content:
                    logger.info(f"  ✓ Generated: {content[:80]}...")
                else:
                    logger.warning(f"  ✗ Failed to generate")
    
    except Exception as e:
        logger.error(f"✗ Content Engine error: {e}")
        import traceback
        traceback.print_exc()

def test_image_generator():
    """Test image generator"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Image Generator")
    logger.info("=" * 60)
    
    try:
        from core.image_generator import ImageGenerator, PlaceholderImageGenerator
        
        # Test DALL-E
        logger.info("\nTesting DALL-E Image Generator...")
        img_gen = ImageGenerator()
        if img_gen.is_enabled():
            logger.info("✓ DALL-E enabled")
            # Don't actually generate (costs money) but show it's ready
            logger.info("  - Status: READY TO GENERATE")
        else:
            logger.warning("✗ DALL-E not enabled (no API key)")
        
        # Test Placeholder
        logger.info("\nTesting Placeholder Image Generator...")
        placeholder = PlaceholderImageGenerator()
        logger.info("✓ Placeholder generator initialized")
        
        # Generate a test placeholder
        image_path = placeholder.generate_placeholder("automation", "pain")
        if image_path:
            logger.info(f"✓ Generated placeholder image: {image_path}")
        else:
            logger.warning("✗ Failed to generate placeholder")
    
    except Exception as e:
        logger.error(f"✗ Image Generator error: {e}")
        import traceback
        traceback.print_exc()

def test_database():
    """Test database connection"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Database")
    logger.info("=" * 60)
    
    try:
        from core.db_init import test_database_connection
        if test_database_connection():
            logger.info("✓ Database connection successful")
        else:
            logger.warning("✗ Database connection failed")
    except Exception as e:
        logger.error(f"✗ Database test error: {e}")

def main():
    """Run all tests"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 15 + "PROMOTION HUB - DEBUG TEST" + " " * 18 + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + " " * 10 + "Testing AI Integration & Core Components" + " " * 8 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    # Run tests
    test_ai_providers()
    test_content_engine()
    test_image_generator()
    test_database()
    
    logger.info("\n" + "=" * 60)
    logger.info("Tests Complete!")
    logger.info("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
