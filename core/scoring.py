"""
Оцінка релевантності лідів.
Вирішує, чи можна:
- зберегти контакт
- запросити
- пропустити
"""

import logging
from typing import Tuple, Dict, List
from enum import Enum

logger = logging.getLogger(__name__)


class LeadDecision(str, Enum):
    """Рішення щодо ліду."""
    INVITE = "invite"
    SAVE = "save"
    SKIP = "skip"


class LeadScorer:
    """Оцінює релевантність лідів для B2B."""
    
    def __init__(
        self,
        threshold_save: float = 0.3,
        threshold_invite: float = 0.6,
    ):
        """
        Ініціалізація скорера.
        
        Args:
            threshold_save: Мінімальний скор для збереження
            threshold_invite: Мінімальний скор для запрошення
        """
        self.threshold_save = threshold_save
        self.threshold_invite = threshold_invite
        
        # B2B ключові слова для пошуку
        self.b2b_keywords = {
            "business", "company", "enterprise", "b2b", "b2c",
            "solutions", "services", "digital", "marketing",
            "consulting", "agency", "management", "software",
            "technology", "IT", "data", "analytics", "automation",
            "entrepreneur", "ceo", "founder", "owner", "director",
            "manager", "professional", "expert", "specialist",
        }
    
    def score_lead(
        self,
        bio: str = "",
        message_content: str = "",
        activity_indicators: Dict = None,
        platform: str = "unknown",
    ) -> Tuple[float, LeadDecision]:
        """
        Оцінює лід.
        
        Args:
            bio: Bio/опис користувача
            message_content: Вміст повідомлень
            activity_indicators: Індикатори активності
            platform: Платформа (instagram, telegram, linkedin)
            
        Returns:
            (скор від 0 до 1, рішення)
        """
        activity_indicators = activity_indicators or {}
        score = 0.0
        details = {
            "platform": platform,
            "factors": []
        }
        
        # 1. Аналіз bio на B2B-ключові слова
        bio_lower = bio.lower()
        b2b_keyword_count = sum(1 for kw in self.b2b_keywords if kw in bio_lower)
        
        if b2b_keyword_count >= 3:
            score += 0.35
            details["factors"].append(f"Bio has {b2b_keyword_count} B2B keywords (+0.35)")
        elif b2b_keyword_count >= 2:
            score += 0.2
            details["factors"].append(f"Bio has {b2b_keyword_count} B2B keywords (+0.2)")
        elif b2b_keyword_count >= 1:
            score += 0.1
            details["factors"].append("Bio has 1 B2B keyword (+0.1)")
        
        # 2. Аналіз повідомлень
        if message_content:
            message_lower = message_content.lower()
            message_b2b_count = sum(1 for kw in self.b2b_keywords if kw in message_lower)
            
            if message_b2b_count >= 3:
                score += 0.25
                details["factors"].append(f"Messages have {message_b2b_count} B2B keywords (+0.25)")
            elif message_b2b_count >= 1:
                score += 0.15
                details["factors"].append("Messages mention B2B topics (+0.15)")
        
        # 3. Активність (залежить від платформи)
        if activity_indicators.get("follower_count", 0) > 100:
            score += 0.1
            details["factors"].append(f"Good follower count ({activity_indicators['follower_count']}) (+0.1)")
        
        if activity_indicators.get("engagement_rate", 0) > 0.05:  # 5% engagement
            score += 0.1
            details["factors"].append(f"Good engagement rate ({activity_indicators['engagement_rate']:.1%}) (+0.1)")
        
        if activity_indicators.get("profile_completeness", 0) > 0.7:
            score += 0.05
            details["factors"].append("Complete profile (+0.05)")
        
        # 4. Тип акаунта (якщо відомо)
        if activity_indicators.get("is_business_account"):
            score += 0.1
            details["factors"].append("Business account (+0.1)")
        
        if activity_indicators.get("is_private"):
            score -= 0.05
            details["factors"].append("Private account (-0.05)")
        
        # Нормалізація скору (0-1)
        score = min(1.0, max(0.0, score))
        details["final_score"] = round(score, 3)
        
        # Визначення рішення
        decision = self._make_decision(score)
        details["decision"] = decision.value
        
        logger.debug(f"Lead scoring: {score:.3f} -> {decision.value} | Factors: {details['factors']}")
        
        return score, decision
    
    def _make_decision(self, score: float) -> LeadDecision:
        """
        Визначає рішення на основі скору.
        
        Args:
            score: Скор релевантності (0-1)
            
        Returns:
            Рішення про ліда
        """
        if score >= self.threshold_invite:
            return LeadDecision.INVITE
        elif score >= self.threshold_save:
            return LeadDecision.SAVE
        else:
            return LeadDecision.SKIP
    
    def batch_score_leads(self, leads: List[Dict]) -> List[Dict]:
        """
        Оцінює партію лідів.
        
        Args:
            leads: Список лідів з полями: bio, message_content, activity_indicators, platform
            
        Returns:
            Список лідів з доданими полями: score, decision
        """
        results = []
        
        for lead in leads:
            score, decision = self.score_lead(
                bio=lead.get("bio", ""),
                message_content=lead.get("message_content", ""),
                activity_indicators=lead.get("activity_indicators", {}),
                platform=lead.get("platform", "unknown"),
            )
            
            lead["score"] = score
            lead["decision"] = decision.value
            results.append(lead)
        
        return results
    
    def get_scoring_report(self, leads: List[Dict]) -> Dict:
        """
        Генерує звіт про оцінку лідів.
        
        Args:
            leads: Список оцінених лідів
            
        Returns:
            Звіт з статистикою
        """
        total = len(leads)
        invites = sum(1 for l in leads if l.get("decision") == "invite")
        saves = sum(1 for l in leads if l.get("decision") == "save")
        skips = sum(1 for l in leads if l.get("decision") == "skip")
        
        avg_score = sum(l.get("score", 0) for l in leads) / total if total > 0 else 0
        
        return {
            "total_leads": total,
            "invites": invites,
            "saves": saves,
            "skips": skips,
            "average_score": round(avg_score, 3),
            "conversion_rate": round(invites / total * 100, 1) if total > 0 else 0,
        }
