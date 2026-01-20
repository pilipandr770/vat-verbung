"""
Аналіз повідомлень і поведінки.
Визначення, чи це B2B-лід.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class TelegramAnalyzer:
    """Аналізує лідів з Telegram."""
    
    def __init__(self):
        """Ініціалізація Telegram analyzer."""
        self.platform = "telegram"
        self.b2b_keywords = {
            "business", "company", "enterprise", "b2b", "marketing",
            "sales", "consulting", "solutions", "services", "project",
            "manager", "founder", "ceo", "owner", "director",
            "digital", "automation", "technology", "software", "data",
        }
    
    def analyze_user(
        self,
        user_id: str,
        username: str,
        bio: str,
        messages: List[str],
        chat_participation: int = 0,
    ) -> Dict:
        """
        Аналізує користувача.
        
        Args:
            user_id: ID користувача
            username: Username користувача
            bio: Bio користувача
            messages: Список повідомлень користувача
            chat_participation: Кількість повідомлень у чатах
            
        Returns:
            Результат аналізу з скором релевантності
        """
        score = 0.0
        reasons = []
        
        # 1. Аналіз bio
        bio_lower = bio.lower()
        b2b_keyword_count = sum(1 for kw in self.b2b_keywords if kw in bio_lower)
        
        if b2b_keyword_count >= 3:
            score += 0.4
            reasons.append(f"Bio has {b2b_keyword_count} B2B keywords")
        elif b2b_keyword_count >= 1:
            score += 0.2
            reasons.append(f"Bio has {b2b_keyword_count} B2B keyword(s)")
        
        # 2. Аналіз повідомлень
        if messages:
            message_text = " ".join(messages).lower()
            message_b2b_keywords = sum(1 for kw in self.b2b_keywords if kw in message_text)
            
            if message_b2b_keywords >= 2:
                score += 0.3
                reasons.append("Messages contain B2B topics")
            elif message_b2b_keywords >= 1:
                score += 0.15
        
        # 3. Активність у чатах
        if chat_participation >= 10:
            score += 0.15
            reasons.append("Active in B2B chats")
        elif chat_participation >= 3:
            score += 0.1
        
        # Нормалізація
        score = min(1.0, max(0.0, score))
        
        is_b2b = b2b_keyword_count >= 1 or "business" in bio_lower
        
        return {
            "user_id": user_id,
            "username": username,
            "score": score,
            "is_b2b": is_b2b,
            "reasons": reasons,
            "recommendation": self._get_recommendation(score, is_b2b),
        }
    
    @staticmethod
    def _get_recommendation(score: float, is_b2b: bool) -> str:
        """Визначає рекомендацію на основі скору."""
        if is_b2b and score >= 0.5:
            return "INVITE"
        elif score >= 0.3:
            return "SAVE"
        else:
            return "SKIP"
