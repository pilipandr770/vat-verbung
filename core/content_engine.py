"""
ЄДИНИЙ контент-завод.
Генерує базовий B2B-контент німецькою мовою (DE)
по темах: ризики, довіра, автоматизація, операційка.
"""

from typing import List, Dict
from enum import Enum


class ContentTopic(str, Enum):
    """Теми контенту."""
    RISKS = "risks"
    TRUST = "trust"
    AUTOMATION = "automation"
    OPERATIONS = "operations"


class ContentEngine:
    """Генератор B2B-контенту німецькою мовою."""
    
    def __init__(self):
        """Ініціалізація контент-генератора."""
        self.language = "de"
        self.content_library = self._init_content_library()
    
    def _init_content_library(self) -> Dict[ContentTopic, List[str]]:
        """Ініціалізація бібліотеки контенту по темам."""
        return {
            ContentTopic.RISKS: [
                "Operationelle Risiken in Ihrem B2B-Prozess: Wie Sie diese minimieren",
                "Compliance-Anforderungen und automatisierte Lösungen",
            ],
            ContentTopic.TRUST: [
                "Vertrauen durch Transparenz: Datengesteuerte Entscheidungen",
                "Sicherheit in der digitalen Transformation",
            ],
            ContentTopic.AUTOMATION: [
                "Automatisierung als Wettbewerbsvorteil",
                "Zeit sparen durch intelligente Prozesse",
            ],
            ContentTopic.OPERATIONS: [
                "Optimierung operationeller Effizienz",
                "Skalierung ohne Chaos: Prozessmanagement",
            ],
        }
    
    def generate_content(
        self,
        topic: ContentTopic,
        style: str = "professional",
    ) -> str:
        """
        Генерує контент за темою.
        
        Args:
            topic: Тема контенту
            style: Стиль презентації (professional, casual)
            
        Returns:
            Згенерований контент німецькою мовою
        """
        content_list = self.content_library.get(topic, [])
        if not content_list:
            return f"Контент для теми {topic} недоступний"
        return content_list[0]
    
    def list_topics(self) -> List[str]:
        """Повертає список доступних тем."""
        return [t.value for t in ContentTopic]
