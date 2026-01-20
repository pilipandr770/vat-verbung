#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Promotion Hub - System Check & Initialization
Validates all configurations before running the main application
"""

import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

class SystemCheck:
    """System configuration checker"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
    
    def check_all(self):
        """Run all checks"""
        logger.info("=" * 60)
        logger.info("🔍 Promotion Hub - System Check")
        logger.info("=" * 60)
        
        self.check_env_file()
        self.check_database()
        self.check_social_credentials()
        self.check_ai_configuration()
        self.check_files_and_dirs()
        self.check_dependencies()
        
        self.print_summary()
        return len(self.errors) == 0
    
    def check_env_file(self):
        """Check if .env file exists and contains required variables"""
        logger.info("\n📋 Checking .env configuration...")
        
        if not Path('.env').exists():
            self.errors.append(".env file not found (copy from .env.example)")
            return
        
        required_vars = [
            'DATABASE_URL',
            'LINKEDIN_USERNAME',
            'LINKEDIN_PASSWORD',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHANNEL_ID',
            'INSTAGRAM_USERNAME',
            'INSTAGRAM_PASSWORD'
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith('your_'):
                self.errors.append(f"   {var} is not configured")
            else:
                logger.info(f"   ✅ {var}")
                self.success_count += 1
    
    def check_database(self):
        """Check database connection"""
        logger.info("\n🗄️  Checking Database...")
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            self.errors.append("DATABASE_URL not configured")
            return
        
        try:
            import psycopg2
            # Don't actually connect here, just validate the URL format
            if 'postgresql://' in db_url:
                logger.info(f"   ✅ Database URL configured")
                self.success_count += 1
            else:
                self.errors.append("Invalid DATABASE_URL format (should start with postgresql://)")
        except ImportError:
            self.errors.append("psycopg2 not installed")
    
    def check_social_credentials(self):
        """Check social media credentials"""
        logger.info("\n📱 Checking Social Credentials...")
        
        # LinkedIn
        li_user = os.getenv('LINKEDIN_USERNAME')
        li_pass = os.getenv('LINKEDIN_PASSWORD')
        if li_user and not li_user.startswith('your_'):
            logger.info(f"   ✅ LinkedIn: {li_user}")
            self.success_count += 1
        else:
            self.warnings.append("LinkedIn credentials incomplete")
        
        # Telegram
        tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
        tg_channel = os.getenv('TELEGRAM_CHANNEL_ID')
        if tg_token and not tg_token.startswith('your_') and tg_channel:
            logger.info(f"   ✅ Telegram: {tg_channel}")
            self.success_count += 1
        else:
            self.warnings.append("Telegram credentials incomplete")
        
        # Instagram
        ig_user = os.getenv('INSTAGRAM_USERNAME')
        ig_session = os.getenv('INSTAGRAM_SESSION')
        if ig_user and not ig_user.startswith('your_'):
            logger.info(f"   ✅ Instagram: {ig_user}")
            self.success_count += 1
            
            # Check if session exists
            if ig_session:
                logger.info(f"   ✅ Instagram session found (.env)")
                self.success_count += 1
            else:
                self.warnings.append(f"Instagram session not found (run: python init_instagram.py)")
        else:
            self.warnings.append("Instagram credentials incomplete")
    
    def check_files_and_dirs(self):
        """Check required files and directories"""
        logger.info("\n📂 Checking Files & Directories...")
        
        required_dirs = ['core', 'channels', 'data', 'logs', 'docs']
        for dir_name in required_dirs:
            if Path(dir_name).exists():
                logger.info(f"   ✅ {dir_name}/")
                self.success_count += 1
            else:
                self.errors.append(f"Missing directory: {dir_name}/")
        
        required_files = [
            'main.py',
            'core/models.py',
            'core/scheduler.py',
            'core/content_engine.py'
        ]
        for file_name in required_files:
            if Path(file_name).exists():
                logger.info(f"   ✅ {file_name}")
                self.success_count += 1
            else:
                self.errors.append(f"Missing file: {file_name}")
    
    def check_dependencies(self):
        """Check Python dependencies"""
        logger.info("\n📦 Checking Dependencies...")
        
        dependencies = [
            ('psycopg2', 'Database'),
            ('dotenv', 'Environment'),
            ('apscheduler', 'Scheduler'),
            ('telegram', 'Telegram'),
            ('instagrapi', 'Instagram'),
            ('playwright', 'LinkedIn'),
            ('openai', 'OpenAI (Optional)'),
            ('google.generativeai', 'Gemini (Optional)'),
            ('PIL', 'Image processing (Optional)')
        ]
        
        for module, name in dependencies:
            try:
                __import__(module)
                logger.info(f"   ✅ {name} ({module})")
                self.success_count += 1
            except ImportError:
                if '(Optional)' in name:
                    self.warnings.append(f"{name} ({module}) not installed - AI features disabled")
                else:
                    self.errors.append(f"{name} ({module}) not installed")
    
    def check_ai_configuration(self):
        """Check AI configuration"""
        logger.info("\n🤖 Checking AI Configuration...")
        
        use_ai = os.getenv('USE_AI_CONTENT', 'False').lower() == 'true'
        
        if not use_ai:
            logger.info(f"   ℹ️  AI content generation disabled (USE_AI_CONTENT=False)")
            self.success_count += 1
            return
        
        ai_provider = os.getenv('AI_PROVIDER', '').lower()
        
        if ai_provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY', '')
            if api_key and api_key.startswith('sk-'):
                logger.info(f"   ✅ OpenAI API key configured")
                self.success_count += 1
            else:
                self.warnings.append("OpenAI API key not configured (USE_AI_CONTENT=True but no key)")
        
        elif ai_provider == 'gemini':
            api_key = os.getenv('GEMINI_API_KEY', '')
            if api_key:
                logger.info(f"   ✅ Gemini API key configured")
                self.success_count += 1
            else:
                self.warnings.append("Gemini API key not configured (USE_AI_CONTENT=True but no key)")
        
        else:
            self.warnings.append(f"Unknown AI_PROVIDER: {ai_provider}")
        
        # Check image generation
        image_api_key = os.getenv('DALLE_API_KEY', '')
        if image_api_key and image_api_key.startswith('sk-'):
            logger.info(f"   ✅ DALL-E API key configured")
            self.success_count += 1
        else:
            logger.info(f"   ℹ️  DALL-E not configured (images will use placeholders)")

    
    def print_summary(self):
        """Print check summary"""
        logger.info("\n" + "=" * 60)
        logger.info(f"✅ Checks Passed: {self.success_count}")
        
        if self.errors:
            logger.error(f"❌ Errors: {len(self.errors)}")
            for error in self.errors:
                logger.error(f"   • {error}")
        
        if self.warnings:
            logger.warning(f"⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                logger.warning(f"   • {warning}")
        
        logger.info("=" * 60)
        
        if self.errors:
            logger.error("\n❌ System check FAILED. Please fix errors above.")
            return False
        elif self.warnings:
            logger.info("\n⚠️  System check passed with warnings.")
            return True
        else:
            logger.info("\n✅ System check PASSED! Ready to run.")
            return True

def main():
    checker = SystemCheck()
    success = checker.check_all()
    
    if success:
        logger.info("\n🚀 To start the system, run:")
        logger.info("   python main.py")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
