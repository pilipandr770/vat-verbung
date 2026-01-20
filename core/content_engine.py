"""
ЄДИНИЙ контент-завод.
Генерує базовий B2B-контент німецькою мовою (DE)
по темах: ризики, довіра, автоматизація, операційка.
"""

import random
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
        self.topic_rotation = list(ContentTopic)
        random.shuffle(self.topic_rotation)
        self.current_topic_index = 0
    
    def _init_content_library(self) -> Dict[ContentTopic, List[str]]:
        """Ініціалізація бібліотеки контенту по темам."""
        return {
            ContentTopic.RISKS: [
                "Operationelle Risiken in Ihrem B2B-Prozess: Wie Sie diese minimieren",
                "Compliance-Anforderungen und automatisierte Lösungen",
                "Datensicherheit: Die unterschätzte Gefahr in der Unternehmenskultur",
                "Fehler in der Supply Chain: Kosten und Präventionsstrategien",
                "Regulatorische Anforderungen: Was Ihr Team wissen muss",
            ],
            ContentTopic.TRUST: [
                "Vertrauen durch Transparenz: Datengesteuerte Entscheidungen",
                "Sicherheit in der digitalen Transformation",
                "Authentizität und Glaubwürdigkeit in B2B-Beziehungen",
                "Wie Sie Kundenbindung durch Konsistenz aufbauen",
                "Ethische KI: Ein Wettbewerbsvorteil für B2B",
            ],
            ContentTopic.AUTOMATION: [
                "Automatisierung als Wettbewerbsvorteil",
                "Zeit sparen durch intelligente Prozesse",
                "Von manuell zu automatisiert: Ein Implementierungsleitfaden",
                "Robotics und RPA: Die Zukunft der operativen Effizienz",
                "Workflow-Automatisierung: ROI in 90 Tagen",
            ],
            ContentTopic.OPERATIONS: [
                "Optimierung operationeller Effizienz",
                "Skalierung ohne Chaos: Prozessmanagement",
                "Metriken, die zählen: KPIs für operative Exzellenz",
                "Lean Operations: Verschwendung eliminieren",
                "Change Management: Transformation ohne Disruption",
            ],
        }
    
    def generate_content(self, topic: ContentTopic = None, style: str = "professional") -> str:
        """
        Генерує контент за темою.
        
        Args:
            topic: Тема контенту (якщо None, вибирається випадково)
            style: Стиль презентації (professional, casual)
            
        Returns:
            Згенерований контент німецькою мовою
        """
        if topic is None:
            topic = random.choice(list(ContentTopic))
        
        content_list = self.content_library.get(topic, [])
        if not content_list:
            return f"Контент для теми {topic} недоступний"
        
        return random.choice(content_list)
    
    def get_random_topic(self) -> ContentTopic:
        """Повертає наступну тему з ротації для уникнення повторення."""
        topic = self.topic_rotation[self.current_topic_index]
        self.current_topic_index = (self.current_topic_index + 1) % len(self.topic_rotation)
        return topic
    
    def list_topics(self) -> List[str]:
        """Повертає список доступних тем."""
        return [t.value for t in ContentTopic]
