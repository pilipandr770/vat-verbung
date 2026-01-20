"""
Публікація постів у Instagram.
"""

import os
import logging
from typing import Optional
from instagrapi import Client

logger = logging.getLogger(__name__)


class InstagramPublisher:
    """Публікатор для Instagram."""
    
    def __init__(self):
        """Ініціалізація Instagram publisher."""
        self.platform = "instagram"
        self.client = Client()
        
        # Завантаження облікових даних
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("INSTAGRAM_USERNAME та INSTAGRAM_PASSWORD мають бути встановлені")
        
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Аутентифікація на Instagram."""
        try:
            logger.info(f"Authenticating to Instagram as {self.username}...")
            self.client.login(self.username, self.password)
            logger.info("✅ Instagram authentication successful")
        except Exception as e:
            logger.error(f"❌ Instagram authentication failed: {e}")
            raise
    
    def publish_post(
        self,
        content: str,
        image_url: Optional[str] = None,
        caption: Optional[str] = None
    ) -> bool:
        """
        Публікує пост на Instagram.
        
        Args:
            content: Адаптований контент (буде використаний як caption)
            image_url: URL зображення (опціонально)
            caption: Текст для caption (якщо не передано, використовується content)
            
        Returns:
            True якщо успішно, False якщо помилка
        """
        try:
            # Якщо image не вказано, публікуємо як карусель-текст або сторис
            if not image_url:
                logger.warning("No image provided, publishing as story or caption-only post")
                return self._publish_text_post(content)
            
            # Якщо є image, завантажуємо і публікуємо
            return self._publish_photo_post(image_url, caption or content)
        
        except Exception as e:
            logger.error(f"❌ Instagram publish error: {e}")
            return False
    
    def _publish_text_post(self, content: str) -> bool:
        """
        Публікує текстовий пост (переважно для Story).
        
        Args:
            content: Текст контенту
            
        Returns:
            True якщо успішно
        """
        try:
            logger.info("Publishing text-based content...")
            # Instagram дозволяє публікувати текст тільки в Stories або як карусель
            # Для карусель потрібні зображення, тому записуємо як запланованого посту
            logger.info(f"Text content: {content[:50]}...")
            logger.info("Note: Text-only posts should be scheduled via Instagram Business API")
            
            # На практиці, потрібні зображення для публічних постів
            return False
        
        except Exception as e:
            logger.error(f"Error publishing text post: {e}")
            return False
    
    def _publish_photo_post(self, image_url: str, caption: str) -> bool:
        """
        Публікує пост з фото.
        
        Args:
            image_url: URL фото
            caption: Текст підпису
            
        Returns:
            True якщо успішно
        """
        try:
            logger.info(f"Downloading image from: {image_url}")
            
            # Завантаження зображення
            import urllib.request
            image_path = "/tmp/instagram_post.jpg"
            urllib.request.urlretrieve(image_url, image_path)
            
            # Публікація
            logger.info("Publishing photo post...")
            self.client.photo_upload(image_path, caption=caption)
            
            logger.info("✅ Photo post published successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error publishing photo post: {e}")
            return False
    
    def schedule_post(
        self,
        content: str,
        image_url: str,
        schedule_time: str,  # ISO format: "2026-01-21T10:00:00"
    ) -> bool:
        """
        Запланує пост на певний час (потребує Business API).
        
        Args:
            content: Текст контенту
            image_url: URL зображення
            schedule_time: Час публікації (ISO format)
            
        Returns:
            True якщо успішно
        """
        try:
            logger.info(f"Scheduling post for: {schedule_time}")
            # TODO: Інтеграція з Instagram Business API для планування
            logger.warning("Scheduling requires Instagram Business API integration")
            return False
        
        except Exception as e:
            logger.error(f"Error scheduling post: {e}")
            return False
