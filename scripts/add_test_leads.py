#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Добавить тестовых лидов в БД для тестирования scoring и invites.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import Lead, DatabaseConnection

load_dotenv()

def add_test_leads():
    """Добавляет тестовых лидов для Telegram."""
    
    db = DatabaseConnection()
    
    # Тестовые лиды
    test_leads = [
        {
            "source": "test",
            "platform": "telegram",
            "identifier": "john_ceo_123",
            "email": "john@company.com",
            "username": "john_ceo",
            "bio": "CEO at Digital Marketing Agency. B2B Solutions & Digital Transformation",
            "score": 0.85,  # High score - will be invited
        },
        {
            "source": "test",
            "platform": "telegram",
            "identifier": "sarah_entrepreneur",
            "email": "sarah@startup.com",
            "username": "sarah_entrepreneur",
            "bio": "Founder & CEO of SaaS startup. Software development solutions",
            "score": 0.75,  # High score
        },
        {
            "source": "test",
            "platform": "telegram",
            "identifier": "mike_business",
            "email": "mike@consulting.com",
            "username": "mike_business",
            "bio": "Business consultant. Enterprise solutions & consulting",
            "score": 0.65,  # Medium-high score
        },
        {
            "source": "test",
            "platform": "telegram",
            "identifier": "anna_personal",
            "email": None,
            "username": "anna_personal",
            "bio": "Love cats and coffee ☕",
            "score": 0.2,  # Low score - won't be invited
        },
    ]
    
    added_count = 0
    
    for lead_data in test_leads:
        try:
            lead = Lead(**lead_data)
            lead_id = lead.save()
            print(f"✅ Added lead: {lead_data['username']} (ID: {lead_id}, Score: {lead_data['score']})")
            added_count += 1
        except Exception as e:
            print(f"⚠️  Error adding {lead_data['username']}: {e}")
            continue
    
    print(f"\n✅ Successfully added {added_count}/{len(test_leads)} test leads")
    print("\nTo test scoring and invites:")
    print("1. Wait for next 'Telegram invite' job to run (every 2-3 hours)")
    print("2. Check logs for invitation results")
    print("3. High-score leads should be marked as 'invited'")

if __name__ == "__main__":
    add_test_leads()
