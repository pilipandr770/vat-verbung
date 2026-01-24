#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final test of the complete publication workflow
"""

import os
from dotenv import load_dotenv
load_dotenv()

from core.content_generator import ContentGenerator
from channels.telegram.publisher import TelegramPublisher
from core.models import Post

def test_complete_workflow():
    """Test the complete content generation and publication workflow."""
    
    print("🎯 FINAL TEST: Complete Publication Workflow")
    print("=" * 50)
    
    # 1. Generate content
    print("1️⃣ Generating content...")
    generator = ContentGenerator()
    content = generator.generate_content()
    
    print(f"   Title: {content['title']}")
    print(f"   Description: {content['description'][:100]}...")
    print(f"   Theme: {content['theme']}")
    print()
    
    # 2. Save to database
    print("2️⃣ Saving to database...")
    post = Post(
        channel="telegram",
        content_de=content['title'],
        content_adapted=content['description'],
    )
    post_id = post.save()
    print(f"   Post saved with ID: {post_id}")
    print()
    
    # 3. Publish to Telegram
    print("3️⃣ Publishing to Telegram...")
    publisher = TelegramPublisher()
    
    # Combine title and description
    full_content = f"{content['title']}\n\n{content['description']}"
    print("   Content to publish:")
    print(f"   {repr(full_content[:150])}...")
    print()
    
    success = publisher.publish_post(full_content)
    
    if success:
        print("✅ Publication successful!")
        post.mark_published()
        print(f"   Post {post_id} marked as published")
    else:
        print("❌ Publication failed")
    
    print()
    print("🎉 Workflow test completed!")

if __name__ == "__main__":
    test_complete_workflow()