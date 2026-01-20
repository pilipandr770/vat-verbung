"""
Follow / акуратний контакт.
Одноразово, без агресивних DM.
"""

import time
import logging
from typing import Dict, Optional
from instagrapi import Client

logger = logging.getLogger(__name__)


class InstagramInviter:
    """Запрошує лідів в Instagram."""
    
    def __init__(self):
        """Ініціалізація Instagram inviter."""
        self.platform = "instagram"
        self.client = Client()
        
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
        
        Args:
            user_id: ID користувача
            username: Username
            bio: Bio користувача
            is_b2b: Чи це B2B-профіль
            
        Returns:
            Dict з результатами: {follow: bool, dm: bool}
        """
        result = {"follow": False, "dm": False}
        
        if not is_b2b:
            logger.info(f"Skipping {username}: not B2B relevant")
            return result
        
        # 1. Follow
        result["follow"] = self.follow_user(user_id, username)
        
        if not result["follow"]:
            logger.warning(f"Skipping DM for {username} due to follow failure")
            return result
        
        # 2. Персоналізоване DM (обережно, один раз!)
        # Витягуємо B2B-ключові слова з bio для персоналізації
        b2b_keywords = ["business", "marketing", "sales", "management", "digital"]
        relevant_keywords = [kw for kw in b2b_keywords if kw in bio.lower()]
        
        if relevant_keywords:
            message = self._create_personalized_message(username, relevant_keywords)
        else:
            message = self._create_default_message()
        
        # Затримка перед DM
        time.sleep(5)
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
