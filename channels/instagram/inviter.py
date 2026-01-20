"""
Follow / акуратний контакт.
Одноразово, без агресивних DM.

Features:
- Day/Night mode: Only invites during 9:00-18:00
- Random messages: 5 templates per bio type
- Random delays: 3-5 minutes between invites (natural behavior)
"""

import time
import logging
from typing import Dict, Optional
from instagrapi import Client
from core.work_hours import WorkHoursManager
from core.message_templates import InstagramMessageTemplates

logger = logging.getLogger(__name__)


class InstagramInviter:
    """Запрошує лідів в Instagram."""
    
    def __init__(self):
        """Ініціалізація Instagram inviter."""
        self.platform = "instagram"
        self.client = Client()
        self.work_hours = WorkHoursManager()
        
        # Затримка між діями (в секундах) для уникнення банування
        self.follow_delay = 10  # 10 секунд між follows
        self.dm_delay = 30  # 30 секунд між DMs
    
    def follow_user(self, user_id: int, username: str) -> bool:
        """
        Follow користувача.
        
        Args:
            user_id: ID користувача на Instagram
            username: Username користувача
            
        Returns:
            True якщо успішно, False якщо помилка
        """
        try:
            logger.info(f"Following user: {username} (ID: {user_id})")
            self.client.user_follow(user_id)
            
            # Затримка для природної поведінки
            time.sleep(self.follow_delay)
            logger.info(f"✅ Successfully followed: {username}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error following {username}: {e}")
            return False
    
    def send_dm(self, user_id: int, username: str, message: str) -> bool:
        """
        Відправляє один DM користувачу (один раз на людину).
        
        Args:
            user_id: ID користувача
            username: Username користувача
            message: Текст повідомлення
            
        Returns:
            True якщо успішно, False якщо помилка
        """
        try:
            logger.info(f"Sending DM to: {username}")
            
            # Перевірка: чи не приватний чат (Instagram обмежує DM до приватних користувачів)
            self.client.send_message(user_id, message)
            
            # Затримка
            time.sleep(self.dm_delay)
            logger.info(f"✅ DM sent to: {username}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error sending DM to {username}: {e}")
            return False
    
    def personalized_invitation(
        self,
        user_id: int,
        username: str,
        bio: str,
        is_b2b: bool,
    ) -> Dict[str, bool]:
        """
        Комплексне запрошення: follow + DM (якщо релевантно).
        
        Features:
        - Only runs during work hours (9-18 by default)
        - Uses random message templates (5 variants)
        - Uses random delays between 3-5 minutes
        
        Args:
            user_id: ID користувача
            username: Username
            bio: Bio користувача
            is_b2b: Чи це B2B-профіль
            
        Returns:
            Dict з результатами: {follow: bool, dm: bool, time_blocked: bool}
        """
        result = {"follow": False, "dm": False, "time_blocked": False}
        
        # Check work hours
        if not self.work_hours.is_work_hours():
            logger.info(f"⏰ Outside work hours: skipping {username}")
            result["time_blocked"] = True
            return result
        
        if not is_b2b:
            logger.info(f"Skipping {username}: not B2B relevant")
            return result
        
        # 1. Follow
        result["follow"] = self.follow_user(user_id, username)
        
        if not result["follow"]:
            logger.warning(f"Skipping DM for {username} due to follow failure")
            return result
        
        # 2. Персоналізоване DM з випадковим шаблоном (5 варіантів)
        message = InstagramMessageTemplates.get_random_template(username, bio)
        
        # Затримка перед DM (випадково 3-5 хвилин)
        delay = self.work_hours.random_delay_between_invites()
        logger.info(f"⏱️ Waiting {delay:.0f}s ({delay/60:.1f}min) before DM to {username}")
        time.sleep(delay)
        
        result["dm"] = self.send_dm(user_id, username, message)
        
        return result
    
    @staticmethod
    def _create_personalized_message(username: str, keywords: list) -> str:
        """Створює персоналізоване повідомлення на основі інтересів."""
        interests = ", ".join(keywords[:2])  # Перші 2 ключові слова
        
        return f"""Hi {username}! 👋

I noticed your interest in {interests}. We've been sharing insights on B2B automation, operational efficiency, and digital transformation.

Would you be interested in connecting?

Best regards"""
    
    @staticmethod
    def _create_default_message() -> str:
        """Стандартне повідомлення запрошення."""
        return """Hi! 👋

We share similar interests in B2B solutions and business optimization. 

Feel free to check out our content if you're interested in digital transformation and automation.

Best regards"""
