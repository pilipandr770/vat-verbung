"""
Оцінка релевантності лідів.
Вирішує, чи можна:
- зберегти контакт
- запросити
- пропустити
"""

from typing import Tuple


class LeadScorer:
    """Оцінює релевантність лідів для B2B."""
    
    def __init__(self, threshold_save: float = 0.3, threshold_invite: float = 0.7):
        """
        Ініціалізація скорера.
        
        Args:
            threshold_save: Мінімальний скор для збереження
            threshold_invite: Мінімальний скор для запрошення
        """
        self.threshold_save = threshold_save
        self.threshold_invite = threshold_invite
    
    def score_lead(
        self,
        bio: str = "",
        message_content: str = "",
        activity_indicators: dict = None,
    ) -> Tuple[float, str]:
        """
        Оцінює лід.
        
        Args:
            bio: Bio/опис користувача
            message_content: Вміст повідомлення
            activity_indicators: Індикатори активності
            
        Returns:
            (скор від 0 до 1, рекомендація)
        """
        activity_indicators = activity_indicators or {}
        score = 0.0
        
        # Аналіз bio
        b2b_keywords = ["business", "company", "b2b", "enterprise", "solutions"]
        if any(kw in bio.lower() for kw in b2b_keywords):
            score += 0.3
        
        # Аналіз активності
        if activity_indicators.get("engagement_rate", 0) > 0.1:
            score += 0.3
        
        if activity_indicators.get("profile_completeness", 0) > 0.7:
            score += 0.2
        
        # Визначення рекомендації
        if score >= self.threshold_invite:
            recommendation = "INVITE"
        elif score >= self.threshold_save:
            recommendation = "SAVE"
        else:
            recommendation = "SKIP"
        
        return score, recommendation
