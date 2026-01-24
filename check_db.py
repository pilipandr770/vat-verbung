#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Status Check
"""

import os
from dotenv import load_dotenv
load_dotenv()

import psycopg2

def check_database():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()

        print("📊 Database Status Check")
        print("=" * 40)

        # Check tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'promotion_hub'")
        tables = cursor.fetchall()
        print("📋 Tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM promotion_hub.{table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} records")

        # Check posts
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.posts WHERE published_at IS NOT NULL")
        published = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.posts")
        total_posts = cursor.fetchone()[0]
        print(f"\n📝 Posts: {published} published / {total_posts} total")

        # Check leads
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.leads WHERE score > 0.5")
        good_leads = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.leads WHERE invited IS NOT NULL")
        invited = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.leads")
        total_leads = cursor.fetchone()[0]
        print(f"🎯 Leads: {good_leads} good (score > 0.5) / {invited} invited / {total_leads} total")

        # Check actions
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.actions")
        actions = cursor.fetchone()[0]
        print(f"⚡ Actions: {actions} total")

        # Recent activity
        cursor.execute("SELECT COUNT(*) FROM promotion_hub.logs WHERE created_at > NOW() - INTERVAL '24 hours'")
        recent_logs = cursor.fetchone()[0]
        print(f"📋 Recent Logs (24h): {recent_logs}")

        conn.close()
        print("\n✅ Database connection successful")

    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database()