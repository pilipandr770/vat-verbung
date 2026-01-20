#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test script to verify AI content generation and posting
Run: python test_content_generation.py
"""

import sys
import os
import logging
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load env vars
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ai_content_generation():
    """Test AI content generation with VAT-Verifizierung focused topics"""
    logger.info("=" * 70)
    logger.info("TEST: AI Content Generation for VAT-Verifizierung Platform")
    logger.info("=" * 70)
    
    try:
        from core.content_engine import ContentEngine, ContentTopic, ContentType
        
        engine = ContentEngine()
        logger.info("[TEST] ContentEngine initialized with VAT-Verifizierung topics")
        
        # Test topics
        test_cases = [
            (ContentTopic.COMPLIANCE, ContentType.PAIN, "Compliance verification pain"),
            (ContentTopic.COMPLIANCE, ContentType.USE_CASE, "Compliance automation success"),
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.PAIN, "Missing OSINT insights"),
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.EXPLANATION, "OSINT explained"),
            (ContentTopic.VERIFICATION, ContentType.PAIN, "Partner verification burden"),
            (ContentTopic.VERIFICATION, ContentType.USE_CASE, "Automated verification"),
            (ContentTopic.INTEGRATION, ContentType.WARNING, "API integration importance"),
            (ContentTopic.SECURITY, ContentType.PAIN, "Link and email security risks"),
            (ContentTopic.EFFICIENCY, ContentType.USE_CASE, "Cost savings with automation"),
            (ContentTopic.TRUST, ContentType.EXPLANATION, "Building trust through transparency"),
            (ContentTopic.DATA_QUALITY, ContentType.PAIN, "CRM data quality issues"),
        ]
        
        success_count = 0
        for i, (topic, ctype, description) in enumerate(test_cases, 1):
            logger.info(f"\n[TEST {i}] {description}")
            logger.info(f"  Topic: {topic.value} | Type: {ctype.value}")
            try:
                content, returned_topic, returned_type = engine.generate_content(
                    topic=topic,
                    content_type=ctype,
                    use_ai=True
                )
                if content and len(content) > 50:
                    success_count += 1
                    logger.info(f"  ✅ Generated {len(content)} chars")
                    logger.info(f"  Preview: {content[:120]}...")
                else:
                    logger.warning(f"  ⚠️  Generated content too short: {len(content) if content else 0} chars")
            except Exception as e:
                logger.warning(f"  ⚠️  Content generation failed: {e}")
        
        logger.info("\n" + "=" * 70)
        logger.info(f"✅ Generated {success_count}/{len(test_cases)} test contents successfully!")
        logger.info("=" * 70)
        return success_count >= len(test_cases) * 0.7  # 70% success rate acceptable
        
    except Exception as e:
        logger.error(f"❌ Content generation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_generation():
    """Test image generation with placeholder"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Image Generation (Placeholder)")
    logger.info("=" * 60)
    
    try:
        from core.image_generator import PlaceholderImageGenerator
        
        generator = PlaceholderImageGenerator()
        logger.info("[TEST] PlaceholderImageGenerator initialized")
        
        # Generate test image
        logger.info("\n[TEST] Generating placeholder image...")
        image_path = generator.generate_placeholder(
            topic="automation",
            content_type="pain"
        )
        logger.info(f"✅ Image generated: {image_path}")
        
        # Check if file exists
        if os.path.exists(image_path):
            size = os.path.getsize(image_path)
            logger.info(f"✅ File size: {size} bytes")
            logger.info("✅ Image generation test PASSED!")
            return True
        else:
            logger.error(f"❌ Image file not found: {image_path}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Image generation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_connection():
    """Test database connection"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Database Connection")
    logger.info("=" * 60)
    
    try:
        import psycopg2
        
        database_url = os.getenv('DATABASE_URL')
        logger.info("[TEST] Attempting database connection...")
        
        conn = psycopg2.connect(database_url)
        logger.info(f"✅ Connected to database: {database_url[:50]}...")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.leads;")
        count = cursor.fetchone()[0]
        logger.info(f"✅ Leads table has {count} records")
        
        conn.close()
        logger.info("✅ Database connection test PASSED!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection test FAILED: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "   PROMOTION HUB - LOCAL TESTING SUITE".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    logger.info("")
    
    results = []
    
    # Run tests
    results.append(("AI Content Generation", test_ai_content_generation()))
    results.append(("Image Generation", test_image_generation()))
    results.append(("Database Connection", test_database_connection()))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n✅ ALL TESTS PASSED - System is ready!")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
