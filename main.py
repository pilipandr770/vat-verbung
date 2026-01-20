#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Promotion Hub - Main Entry Point
Single command to run the entire automation system
"""

import logging
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Auto-generate .env from Render environment variables if not present
env_file = Path(__file__).parent / ".env"
if not env_file.exists():
    from setup_env import create_env_from_environment
    create_env_from_environment()

# Load environment variables first
load_dotenv()

# Setup logging from env
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file = os.getenv('LOG_FILE', 'logs/promotion_hub.log')

# Ensure logs directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Create custom stream handler that handles Unicode
class UnicodeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            # Replace emojis with [emoji]
            msg = msg.replace('✅', '[OK]').replace('🤖', '[BOT]').replace('🔍', '[SEARCH]')
            self.stream.write(msg + '\n')
            self.flush()
        except Exception:
            self.handleError(record)

# Configure logging
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        UnicodeStreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print welcome banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                  PROMOTION HUB v1.0                       ║
║          B2B Marketing Automation Platform                ║
║                                                           ║
║  Channels: LinkedIn • Instagram • Telegram               ║
║  Database: PostgreSQL • Scheduler: APScheduler           ║
║  Language: German (DE) • Audience: B2B Only              ║
╚═══════════════════════════════════════════════════════════╝
    """
    logger.info(banner)

def main():
    """Main entry point"""
    print_banner()
    
    try:
        # Step 1: System check
        logger.info("🔍 Running pre-flight checks...")
        from system_check import SystemCheck
        checker = SystemCheck()
        if not checker.check_all():
            logger.error("❌ System check failed. Please fix errors above.")
            return 1
        
        logger.info("✅ All systems ready!")
        
        # Step 2: Initialize database
        logger.info("\n📦 Initializing database...")
        from core.db_init import init_database
        init_database()
        logger.info("✅ Database initialized")
        
        # Step 3: Start scheduler
        logger.info("\n🚀 Starting scheduler...")
        from core.scheduler import Scheduler
        scheduler = Scheduler()
        
        logger.info("=" * 60)
        logger.info("✅ PROMOTION HUB STARTED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info("\n📊 Scheduled Jobs:")
        logger.info("   • LinkedIn: 2x daily (08:00, 15:00)")
        logger.info("   • Instagram: 3x daily (09:00, 13:00, 19:00)")
        logger.info("   • Telegram: 5x daily (08:00, 11:00, 14:00, 17:00, 20:00)")
        logger.info("   • Lead Collection: Every 6-8 hours")
        logger.info("   • Lead Invitations: Every 2-3 hours")
        logger.info("\n💡 Tips:")
        logger.info("   • Press Ctrl+C to stop gracefully")
        logger.info("   • Check logs/promotion_hub.log for details")
        logger.info("   • Monitor database with SQL client")
        logger.info("=" * 60 + "\n")
        
        # Run scheduler (blocking)
        scheduler.run()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Shutdown requested by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
