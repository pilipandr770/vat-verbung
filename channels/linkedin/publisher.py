"""
Публікація постів на LinkedIn-сторінці.
НІЯКОГО outreach і DM.
"""


class LinkedInPublisher:
    """Публікатор для LinkedIn."""
    
    def __init__(self):
        """Ініціалізація LinkedIn publisher."""
        self.platform = "linkedin"
        self.api_client = None  # TODO: Інтеграція з LinkedIn API
    
    def publish_post(self, content: str) -> bool:
        """
        Публікує пост на сторінці.
        
        Args:
            content: Адаптований контент
            
        Returns:
            True якщо публікація успішна
        """
        # НІЯКИХ DM, тільки пости на сторінці
        print(f"[LinkedIn] Публікація: {content[:50]}...")
        return True
