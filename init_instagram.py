#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Session Initializer
Initializes Instagram session and saves it for later use
"""

import os
import sys
import pickle
import logging
from pathlib import Path
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, BadPassword

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

def init_instagram_session():
    """Initialize and save Instagram session"""
    
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    session_file = os.getenv('INSTAGRAM_SESSION_FILE', 'instagram_session.pkl')
    
    if not username or not password:
        logger.error("❌ INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD not set in .env")
        return False
    
    logger.info(f"🔄 Initializing Instagram session for {username}...")
    
    try:
        # Create client
        cl = Client()
        
        # Try to login
        logger.info("📱 Logging in...")
        cl.login(username, password)
        
        logger.info("✅ Login successful!")
        
        # Save session
        session_file_path = Path(session_file)
        session_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(session_file_path, 'wb') as f:
            pickle.dump(cl.get_settings(), f)
        
        logger.info(f"💾 Session saved to {session_file}")
        
        # Test connection
        logger.info("🧪 Testing connection...")
        try:
            # Get account info via API
            account_info = cl.account_info()
            logger.info(f"✅ Connected as: @{account_info.username}")
            logger.info(f"   User ID: {account_info.pk}")
            logger.info(f"   Bio: {account_info.biography[:50] if account_info.biography else 'No bio'}")
        except Exception as e:
            logger.warning(f"⚠️  Could not fetch full account info: {str(e)}")
            logger.info(f"✅ Session is valid (user_id: {cl.user_id})")
        
        logger.info("=" * 60)
        logger.info("✅ SESSION INITIALIZED SUCCESSFULLY!")
        logger.info(f"   File: {session_file}")
        logger.info(f"   Status: Ready to use")
        logger.info("=" * 60)
        
        return True
        
    except BadPassword:
        logger.error("❌ Wrong username or password")
        return False
    except LoginRequired:
        logger.error("❌ Instagram requires additional authentication (2FA, Email verification)")
        logger.error("   Please check your email or app for verification code")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        logger.error(f"   Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = init_instagram_session()
    sys.exit(0 if success else 1)
