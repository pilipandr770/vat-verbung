"""
Оркестратор.
Визначає:
- коли публікувати контент
- коли запускати збір ЦА
- коли запускати запрошення
"""

from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    """Керує планування і оркестрацією всіх каналів."""
    
    def __init__(self):
        """Ініціалізація scheduler."""
        self.is_running = False
        self.channels = ["linkedin", "telegram", "instagram"]
    
    def run(self) -> None:
        """Запуск головного цикла."""
        self.is_running = True
        logger.info("Promotion Hub Scheduler запущений")
        
        try:
            while self.is_running:
                self._execute_cycle()
        except KeyboardInterrupt:
            logger.info("Scheduler зупинений користувачем")
            self.is_running = False
    
    def _execute_cycle(self) -> None:
        """Виконання одного циклу оркестрації."""
        logger.info(f"Цикл {datetime.now()}: перевірка всіх каналів")
        
        for channel in self.channels:
            logger.info(f"  Обробка каналу: {channel}")
            # TODO: Виконання операцій для кожного каналу
    
    def stop(self) -> None:
        """Зупинення scheduler."""
        self.is_running = False
        logger.info("Scheduler зупинений")
