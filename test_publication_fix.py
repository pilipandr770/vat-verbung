#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test publication workflow fix
"""

import os
from dotenv import load_dotenv
load_dotenv()

from core.scheduler import Scheduler
from core.models import DatabaseConnection

def test_publication():
    """Test publication workflow with database status updates."""

    print("🧪 Testing Publication Workflow")
    print("=" * 40)

    # Initialize scheduler (this will load all publishers)
    scheduler = Scheduler()

    # Manually trigger Telegram publication
    print("\n📱 Testing Telegram publication...")
    try:
        scheduler._publish_telegram()
        print("✅ Telegram publication test completed")
    except Exception as e:
        print(f"❌ Telegram publication failed: {e}")

    # Check database status
    print("\n📊 Checking database status...")
    db = DatabaseConnection()
    with db.get_cursor() as cur:
        cur.execute('SELECT COUNT(*) as total FROM posts')
        total_posts = cur.fetchone()['total']

        cur.execute('SELECT COUNT(*) as published FROM posts WHERE published = TRUE')
        published_posts = cur.fetchone()['published']

        print(f"Всего постов: {total_posts}")
        print(f"Опубликованных: {published_posts}")

        if published_posts > 0:
            print("\n✅ SUCCESS: Posts are being marked as published!")
            cur.execute('SELECT id, channel, published_at FROM posts WHERE published = TRUE ORDER BY published_at DESC LIMIT 1')
            post = cur.fetchone()
            print(f"Последний опубликованный пост: ID {post['id']} ({post['channel']}) в {post['published_at']}")
        else:
            print("\n❌ ISSUE: No posts marked as published")

if __name__ == "__main__":
    test_publication()