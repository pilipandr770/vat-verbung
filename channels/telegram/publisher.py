"""
Публікація постів у наш Telegram-канал.
"""

import os
import logging
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramPublisher:
    """Публікатор для Telegram-каналу."""
    
    def __init__(self):
        """Ініціалізація Telegram publisher."""
        self.platform = "telegram"
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
        
        if not self.bot_token or not self.channel_id:
            raise ValueError("TELEGRAM_BOT_TOKEN та TELEGRAM_CHANNEL_ID мають бути встановлені")
        
        self.bot = Bot(token=self.bot_token)
    
    def publish_post(
        self,
        content: str,
        image_url: Optional[str] = None,
        schedule_time: Optional[str] = None,
    ) -> bool:
        """
        Публікує пост у Telegram канал.
        
        Args:
            content: Адаптований контент
            image_url: URL зображення (опціонально)
            schedule_time: Час публікації (опціонально, ISO format)
            
        Returns:
            True якщо успішно, False якщо помилка
        """
        try:
            if image_url:
                return self._publish_photo(content, image_url)
            else:
                return self._publish_text(content)
        
        except Exception as e:
            logger.error(f"❌ Telegram publish error: {e}")
            return False
    
    def _publish_text(self, content: str) -> bool:
        """
        Публікує текстовий пост.
        
        Args:
            content: Текст контенту
            
        Returns:
            True якщо успішно
        """
        try:
            logger.info("Publishing text post to Telegram...")
            
            self.bot.send_message(
                chat_id=self.channel_id,
                text=content,
                parse_mode="HTML",  # Підтримання HTML форматування
            )
            
            logger.info("✅ Text post published successfully")
            return True
        
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    def _publish_photo(self, caption: str, photo_url: str) -> bool:
        """
        Публікує пост з фото.
        
        Args:
            caption: Текст під фото
            photo_url: URL фото
            
        Returns:
            True якщо успішно
        """
        try:
            logger.info("Publishing photo post to Telegram...")
            
            self.bot.send_photo(
                chat_id=self.channel_id,
                photo=photo_url,
                caption=caption,
                parse_mode="HTML",
            )
            
            logger.info("✅ Photo post published successfully")
            return True
        
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    def publish_article(
        self,
        title: str,
        content: str,
        url: Optional[str] = None,
    ) -> bool:
        """
        Публікує статтю у форматі посилання.
        
        Args:
            title: Заголовок статті
            content: Короткий опис
            url: Посилання на повну статтю
            
        Returns:
            True якщо успішно
        """
        try:
            message = f"""<b>{title}</b>

{content}"""
            
            if url:
                message += f"\n\n<a href='{url}'>Read more →</a>"
            
            return self._publish_text(message)
        
        except Exception as e:
            logger.error(f"Error publishing article: {e}")
            return False
