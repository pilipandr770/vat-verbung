"""
Адаптація одного й того ж контенту
під формат LinkedIn / Telegram / Instagram.
"""

from typing import Dict


class ContentAdapter:
    """Адаптує базовий контент під різні платформи."""
    
    def __init__(self):
        """Ініціалізація адаптера."""
        self.adapters = {
            "linkedin": self._adapt_to_linkedin,
            "telegram": self._adapt_to_telegram,
            "instagram": self._adapt_to_instagram,
        }
    
    def adapt(self, content_de: str, platform: str) -> str:
        """
        Адаптує контент під платформу.
        
        Args:
            content_de: Базовий контент німецькою
            platform: Платформа (linkedin, telegram, instagram)
            
        Returns:
            Адаптований контент
        """
        adapter = self.adapters.get(platform)
        if not adapter:
            raise ValueError(f"Невідома платформа: {platform}")
        return adapter(content_de)
    
    @staticmethod
    def _adapt_to_linkedin(content_de: str) -> str:
        """Адаптація для LinkedIn (професійний тон, довгі пости)."""
        return f"""
🔍 B2B Insights

{content_de}

#B2B #DigitalTransformation #BusinessOptimization #Germany
""".strip()
    
    @staticmethod
    def _adapt_to_telegram(content_de: str) -> str:
        """Адаптація для Telegram (коротше, з emoji)."""
        return f"""
📌 {content_de}

🔗 Детальніше у нашому каналі
""".strip()
    
    @staticmethod
    def _adapt_to_instagram(content_de: str) -> str:
        """Адаптація для Instagram (візуальна, з hashtags)."""
        return f"""
✨ {content_de}

#B2B #Automation #DigitalTransformation #BusinessGrowth
""".strip()
