"""
Єдина точка входу проєкту Promotion Hub.
Запускає scheduler, який керує всіма каналами.
"""

import logging
import sys
from core.db_init import init_database
from core.scheduler import Scheduler


# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Запуск основного цикла Promotion Hub."""
    try:
        # 1. Ініціалізація БД (якщо потрібно)
        logger.info("Initializing database...")
        init_database()
        logger.info("Database ready")
        
        # 2. Запуск scheduler
        logger.info("Starting Promotion Hub Scheduler...")
        scheduler = Scheduler()
        scheduler.run()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
