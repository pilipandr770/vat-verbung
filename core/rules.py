"""
Політики і обмеження.
Антиспам-правила:
- 1 контакт = 1 запрошення
- ліміти дій
- затримки
"""

from datetime import datetime, timedelta
from typing import Dict, Set


class RulesEngine:
    """Антиспам-movimento та управління обмеженнями."""
    
    def __init__(self):
        """Ініціалізація règles."""
        # Один контакт = одне запрошення
        self.invited_contacts: Set[str] = set()
        
        # Ліміти за день на канал
        self.daily_limits = {
            "linkedin": {"posts": 2, "actions": 50},
            "telegram": {"posts": 5, "invites": 10},
            "instagram": {"posts": 3, "invites": 8},
        }
        
        # Затримки між діями (в секундах)
        self.action_delays = {
            "post": 3600,  # 1 година
            "invite": 300,  # 5 хвилин
            "collect": 60,  # 1 хвилина
        }
        
        # Логування дій
        self.action_log: Dict[str, list] = {}
    
    def can_invite(self, contact_id: str) -> bool:
        """
        Перевірка: чи можна запросити цей контакт.
        
        Args:
            contact_id: ID контакту
            
        Returns:
            True якщо контакт ще не запрошувався
        """
        return contact_id not in self.invited_contacts
    
    def mark_invited(self, contact_id: str) -> None:
        """
        Позначити контакт як запрошений.
        
        Args:
            contact_id: ID контакту
        """
        self.invited_contacts.add(contact_id)
    
    def check_daily_limit(self, channel: str, action_type: str) -> bool:
        """
        Перевірка добового ліміту.
        
        Args:
            channel: Канал (linkedin, telegram, instagram)
            action_type: Тип дії (posts, invites)
            
        Returns:
            True якщо ліміт не перевищений
        """
        today = datetime.now().date()
        log_key = f"{channel}_{action_type}_{today}"
        
        count = len(self.action_log.get(log_key, []))
        limit = self.daily_limits.get(channel, {}).get(action_type, 0)
        
        return count < limit
    
    def log_action(self, channel: str, action_type: str) -> None:
        """
        Логувати дію.
        
        Args:
            channel: Канал
            action_type: Тип дії
        """
        today = datetime.now().date()
        log_key = f"{channel}_{action_type}_{today}"
        
        if log_key not in self.action_log:
            self.action_log[log_key] = []
        
        self.action_log[log_key].append(datetime.now())
