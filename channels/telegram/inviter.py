"""
Акуратне додавання / контакт.
Без масових розсилок.

Features:
- Day/Night mode: Only invites during 9:00-18:00
- Random messages: 5 templates per bio type
- Random delays: 3-5 minutes between invites (natural behavior)
"""

import os
import time
import logging
from typing import Dict
from telegram import Bot
from telegram.error import TelegramError
from core.work_hours import WorkHoursManager
from core.message_templates import TelegramMessageTemplates

logger = logging.getLogger(__name__)


class TelegramInviter:
    """Запрошує лідів в Telegram."""
    
    def __init__(self):
        """Ініціалізація Telegram inviter."""
        self.platform = "telegram"
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.work_hours = WorkHoursManager()
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN має бути встановлена")
        
        self.bot = Bot(token=self.bot_token)
        self.message_delay = 300  # 5 хвилин затримка між запрошеннями
    
    def send_invite(self, user_id: str, username: str, bio: str) -> Dict:
        """
        Відправляє персоналізоване запрошення.
        
        Features:
        - Only runs during work hours (9-18 by default)
        - Uses random message templates (5 variants)
        - Uses random delays between 3-5 minutes
        
        Args:
            user_id: ID користувача
            username: Username користувача
            bio: Bio для персоналізації
            
        Returns:
            Dict з результатом відправки
        """
        try:
            # Check work hours
            if not self.work_hours.is_work_hours():
                logger.info(f"⏰ Outside work hours: skipping {username}")
                return {
                    "success": False,
                    "user_id": user_id,
                    "username": username,
                    "error": "Outside work hours (9:00-18:00)",
                    "time_blocked": True,
                }
            
            # Get random message template (5 variants available)
            message = TelegramMessageTemplates.get_random_template(username, bio)
            
            logger.info(f"Sending invite to: {username} (ID: {user_id})")
            
            # Відправка повідомлення
            self.bot.send_message(chat_id=user_id, text=message)
            
            # Random delay between 3-5 minutes for natural behavior
            delay = self.work_hours.random_delay_between_invites()
            logger.info(f"⏱️ Waiting {delay:.0f}s ({delay/60:.1f}min) before next invite")
            time.sleep(delay)
            
            logger.info(f"✅ Invite sent to: {username}")
            
            return {
                "success": True,
                "user_id": user_id,
                "username": username,
            }
        
        except TelegramError as e:
            logger.error(f"❌ Telegram error sending to {username}: {e}")
            return {
                "success": False,
                "user_id": user_id,
                "username": username,
                "error": str(e),
            }
        
        except Exception as e:
            logger.error(f"❌ Error inviting {username}: {e}")
            return {
                "success": False,
                "user_id": user_id,
                "username": username,
                "error": str(e),
            }
    
    @staticmethod
    def _create_personalized_message(username: str, bio: str) -> str:
        """
        Створює персоналізоване запрошення.
        
        Args:
            username: Username користувача
            bio: Bio для аналізу
            
        Returns:
            Текст повідомлення
        """
        bio_lower = bio.lower()
        
        # Вибір шаблону на основі bio
        if "marketing" in bio_lower:
            template = """Hi {name}! 👋

I noticed your interest in marketing and B2B growth.

We're sharing insights on digital transformation, automation, and operational efficiency. 

Would you be interested in connecting?

Best regards"""
        
        elif "business" in bio_lower or "sales" in bio_lower:
            template = """Hi {name}! 🤝

Your business perspective is interesting to us.

We've been discussing B2B automation and process optimization. Would you like to join the conversation?

Best regards"""
        
        else:
            template = """Hi {name}! 👋

I think you'd enjoy our community focused on B2B growth and digital solutions.

Feel free to reach out if you're interested!

Best regards"""
        
        return template.format(name=username)
