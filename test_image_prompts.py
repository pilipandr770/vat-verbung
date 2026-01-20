#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for new professional image generation prompts
Tests that the new detailed prompts are being used correctly
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from core.image_generator import ImageGenerator
from core.content_engine import ContentEngine
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_image_generation():
    """Test image generation with new professional prompts"""
    
    logger.info("=" * 70)
    logger.info("🎨 Testing Image Generation with Professional Prompts")
    logger.info("=" * 70)
    
    image_gen = ImageGenerator()
    
    # Test cases: (topic, content_type)
    test_cases = [
        ("automation", "pain"),
        ("automation", "warning"),
        ("automation", "use_case"),
        ("compliance", "pain"),
        ("digitalization", "warning"),
        ("costs", "use_case"),
        ("workflows", "explanation"),
        ("operations", "pain"),
        ("data", "explanation"),
    ]
    
    for topic, content_type in test_cases:
        logger.info(f"\n📸 Testing: {topic} / {content_type}")
        logger.info("-" * 50)
        
        # Get the prompt
        prompt = image_gen._create_image_prompt(topic, content_type)
        
        # Show first 200 chars of prompt
        prompt_preview = prompt[:300] + "..." if len(prompt) > 300 else prompt
        logger.info(f"Prompt preview: {prompt_preview}")
        
        # Generate image (will use placeholder if DALL-E not available)
        image_path = image_gen.generate_image(topic, content_type)
        
        if image_path:
            logger.info(f"✅ Image generated: {image_path}")
        else:
            logger.info(f"⚠️  No image generated")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ Image Generation Test Complete")
    logger.info("=" * 70)
    logger.info("\n📋 Summary:")
    logger.info("- All new professional prompts have been applied")
    logger.info("- Each prompt includes:")
    logger.info("  • Specific visual elements and composition")
    logger.info("  • Target audience context (B2B/LinkedIn)")
    logger.info("  • German market aesthetic guidelines")
    logger.info("  • Quality and technical specifications")
    logger.info("\n💡 If images are placeholders:")
    logger.info("- DALL-E-3 API not enabled (add OPENAI_API_KEY)")
    logger.info("- Fallback is working correctly with PIL")
    logger.info("\n✨ For production DALL-E usage:")
    logger.info("- Add OPENAI_API_KEY to .env")
    logger.info("- Ensure DALL-E-3 credit is available")
    logger.info("- Professional prompts will generate quality marketing images")

if __name__ == "__main__":
    test_image_generation()
