#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Session Loader & Tester
Loads Instagram session from .env and tests connection
"""

import os
import json
import base64
import logging
from dotenv import load_dotenv
from instagrapi import Client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

def load_instagram_session():
    """Load Instagram session from .env"""
    
    session_b64 = os.getenv('INSTAGRAM_SESSION')
    
    if not session_b64:
        logger.error(f"❌ INSTAGRAM_SESSION not found in .env")
        logger.info("📝 Run: python init_instagram.py")
        return None
    
    logger.info(f"📂 Loading session from .env...")
    
    try:
        cl = Client()
        
        # Decode and load session
        session_json = base64.b64decode(session_b64).decode()
        session_data = json.loads(session_json)
        cl.set_settings(session_data)
        
        logger.info("✅ Session loaded!")
        
        # Test connection
        logger.info("🧪 Testing connection...")
        try:
            account = cl.account_info()
            logger.info(f"✅ Connected as: @{account.username}")
            logger.info(f"   User ID: {account.pk}")
            logger.info(f"   Bio: {account.biography[:50] if account.biography else 'No bio'}")
            return cl
        except Exception as e:
            logger.warning(f"⚠️  Session may have expired: {str(e)}")
            logger.info("🔄 Please run: python init_instagram.py")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error loading session: {str(e)}")
        return None

if __name__ == "__main__":
    client = load_instagram_session()
    if client:
        logger.info("\n✅ Session is ready to use!")
    else:
        logger.error("\n❌ Could not load session")
