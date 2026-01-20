#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Session Initializer
Initializes Instagram session and saves it to .env
"""

import os
import sys
import json
import base64
import logging
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
    """Initialize and save Instagram session to .env"""
    
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    env_file = '.env'
    
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
        
        # Save session to .env as base64 encoded JSON
        logger.info("💾 Saving session to .env...")
        try:
            session_data = cl.get_settings()
            session_json = json.dumps(session_data, default=str)
            session_b64 = base64.b64encode(session_json.encode()).decode()
            
            # Update .env file
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    env_content = f.read()
                
                # Replace or add INSTAGRAM_SESSION
                if 'INSTAGRAM_SESSION=' in env_content:
                    env_content = env_content.replace(
                        env_content.split('INSTAGRAM_SESSION=')[0] + 'INSTAGRAM_SESSION=' + env_content.split('INSTAGRAM_SESSION=')[1].split('\n')[0],
                        f'INSTAGRAM_SESSION={session_b64}'
                    )
                else:
                    env_content += f'\nINSTAGRAM_SESSION={session_b64}\n'
                
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(env_content)
            
            logger.info("✅ Session saved to .env")
            
        except Exception as e:
            logger.warning(f"⚠️  Could not save session to .env: {str(e)}")
            return False
        
        # Test connection
        logger.info("🧪 Testing connection...")
        try:
            account = cl.account_info()
            logger.info(f"✅ Connected as: @{account.username}")
            logger.info(f"   User ID: {account.pk}")
            logger.info(f"   Bio: {account.biography[:50] if account.biography else 'No bio'}")
        except Exception as e:
            logger.warning(f"⚠️  Could not fetch account info: {str(e)}")
            logger.info(f"✅ Session is valid (user_id: {cl.user_id})")
        
        logger.info("=" * 60)
        logger.info("✅ SESSION INITIALIZED SUCCESSFULLY!")
        logger.info(f"   Saved to: .env (INSTAGRAM_SESSION)")
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
