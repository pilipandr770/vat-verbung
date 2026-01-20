"""
ЄДИНИЙ контент-завод.
Генерує базовий B2B-контент німецькою мовою (DE)
по темах: ризики, довіра, автоматизація, операційка.

Контент має різні типи: pain (проблеми), warning (попередження),
use-case (прикладифоів), explanation (пояснення).
"""

import random
from typing import List, Dict, Tuple
from enum import Enum


class ContentTopic(str, Enum):
    """Теми контенту."""
    RISKS = "risks"
    TRUST = "trust"
    AUTOMATION = "automation"
    OPERATIONS = "operations"


class ContentType(str, Enum):
    """Типи контенту."""
    PAIN = "pain"           # Проблема/больовий пункт
    WARNING = "warning"     # Попередження/ризик
    USE_CASE = "use_case"   # Приклад з реальної практики
    EXPLANATION = "explanation"  # Пояснення концепції


class ContentEngine:
    """Генератор B2B-контенту німецькою мовою."""
    
    def __init__(self):
        """Ініціалізація контент-генератора."""
        self.language = "de"
        self.content_library = self._init_content_library()
        self.topic_rotation = list(ContentTopic)
        self.content_type_rotation = list(ContentType)
        random.shuffle(self.topic_rotation)
        random.shuffle(self.content_type_rotation)
        self.topic_index = 0
        self.type_index = 0
    
    def _init_content_library(self) -> Dict[ContentTopic, Dict[ContentType, List[str]]]:
        """Ініціалізація структурованої бібліотеки контенту."""
        return {
            ContentTopic.RISKS: {
                ContentType.PAIN: [
                    "Operationelle Risiken in Ihrem B2B-Prozess: Wie Sie diese minimieren",
                    "Versteckte Kostenfallen in Ihrer Supply Chain: Was Sie ignoriert haben",
                    "Datenlecks und Compliance-Bußgelder: Die unterschätzte Bedrohung",
                ],
                ContentType.WARNING: [
                    "Compliance-Anforderungen und automatisierte Lösungen",
                    "Regulatorische Anforderungen: Was Ihr Team wissen muss",
                    "Fehler in der Supply Chain: Kosten und Präventionsstrategien",
                ],
                ContentType.USE_CASE: [
                    "Wie ein Unternehmen seine Risiken um 40% reduzierte",
                    "Fallstudie: Von Prozesschaos zu automatisierter Sicherheit",
                    "Praktisches Beispiel: Fehlerquote von 25% auf 2% gesenkt",
                ],
                ContentType.EXPLANATION: [
                    "Operationelles Risikomanagement verstehen: Ein Leitfaden",
                    "Warum Automatisierung Ihre Risiken minimiert",
                    "Die Rolle der Transparenz im Risikomanagement",
                ],
            },
            ContentTopic.TRUST: {
                ContentType.PAIN: [
                    "Vertrauen durch Transparenz: Datengesteuerte Entscheidungen",
                    "Authentizität und Glaubwürdigkeit in B2B-Beziehungen",
                    "Warum Ihre Kunden nicht Ihnen vertrauen (und wie Sie das ändern)",
                ],
                ContentType.WARNING: [
                    "Sicherheit in der digitalen Transformation",
                    "Ethische KI: Ein Wettbewerbsvorteil für B2B",
                    "Konsistenz als Grundlage für Geschäftsvertrauen",
                ],
                ContentType.USE_CASE: [
                    "Wie transparente Daten die Kundenbeziehung verbesserten",
                    "Fallbeispiel: Kundenvertrauen durch automatisierte Reports",
                    "Authentisches Marketing: Von Skeptikern zu Partnern",
                ],
                ContentType.EXPLANATION: [
                    "Vertrauensaufbau im B2B: Strategien und Best Practices",
                    "Sicherheit und Vertrauen: Warum beide notwendig sind",
                    "Datenverarbeitung transparent gestalten",
                ],
            },
            ContentTopic.AUTOMATION: {
                ContentType.PAIN: [
                    "Manuelle Prozesse kosten Ihnen Millionen: Erkenne den Preis",
                    "Zeit sparen durch intelligente Prozesse",
                    "Menschliche Fehler in der Produktion: Ein kostspieliges Problem",
                ],
                ContentType.WARNING: [
                    "Von manuell zu automatisiert: Ein Implementierungsleitfaden",
                    "Robotics und RPA: Die Zukunft der operativen Effizienz",
                    "Automatisierung: Nicht optional, sondern notwendig",
                ],
                ContentType.USE_CASE: [
                    "ROI in 90 Tagen: Workflow-Automatisierung im Einzelhandel",
                    "Fallstudie: Von 5 Tagen Bearbeitung auf 1 Stunde",
                    "Praktisches Beispiel: 10.000 Stunden pro Jahr gespart",
                ],
                ContentType.EXPLANATION: [
                    "Automatisierungsarten verstehen: RPA, BPM, ML",
                    "Wie Automatisierung Ihre Wettbewerbsfähigkeit verbessert",
                    "Implementation vs. Tool-Auswahl: Was zuerst?",
                ],
            },
            ContentTopic.OPERATIONS: {
                ContentType.PAIN: [
                    "Optimierung operationeller Effizienz",
                    "Skalierung ohne Chaos: Prozessmanagement",
                    "Bottlenecks in Ihrer Operationen: Wie man sie erkennt",
                ],
                ContentType.WARNING: [
                    "Metriken, die zählen: KPIs für operative Exzellenz",
                    "Lean Operations: Verschwendung eliminieren",
                    "Change Management: Transformation ohne Disruption",
                ],
                ContentType.USE_CASE: [
                    "Operationen skaliert: Von 10 zu 100 Mitarbeitern ohne Chaos",
                    "Fallstudie: Lean Methoden im SaaS-Unternehmen",
                    "Prozessoptimierung: 30% Kostenreduktion in 6 Monaten",
                ],
                ContentType.EXPLANATION: [
                    "Operational Excellence Framework",
                    "Metriken und KPIs: Was Sie messen sollten",
                    "Continuous Improvement: Methoden und Best Practices",
                ],
            },
        }
    
    def generate_content(
        self,
        topic: ContentTopic = None,
        content_type: ContentType = None,
        style: str = "professional",
    ) -> Tuple[str, ContentTopic, ContentType]:
        """
        Генерує контент за темою й типом.
        
        Args:
            topic: Тема контенту (якщо None, вибирається з ротації)
            content_type: Тип контенту (якщо None, вибирається з ротації)
            style: Стиль презентації (professional, casual)
            
        Returns:
            (текст контенту, тема, тип)
        """
        if topic is None:
            topic = self.get_random_topic()
        
        if content_type is None:
            content_type = self.get_random_content_type()
        
        content_list = self.content_library.get(topic, {}).get(content_type, [])
        
        if not content_list:
            return (
                f"Content for {topic.value}/{content_type.value} is not available",
                topic,
                content_type,
            )
        
        content = random.choice(content_list)
        return content, topic, content_type
    
    def get_random_topic(self) -> ContentTopic:
        """Повертає наступну тему з ротації для уникнення повторення."""
        topic = self.topic_rotation[self.topic_index]
        self.topic_index = (self.topic_index + 1) % len(self.topic_rotation)
        return topic
    
    def get_random_content_type(self) -> ContentType:
        """Повертає наступний тип контенту з ротації."""
        ctype = self.content_type_rotation[self.type_index]
        self.type_index = (self.type_index + 1) % len(self.content_type_rotation)
        return ctype
    
    def list_topics(self) -> List[str]:
        """Повертає список доступних тем."""
        return [t.value for t in ContentTopic]
    
    def list_content_types(self) -> List[str]:
        """Повертає список доступних типів контенту."""
        return [t.value for t in ContentType]
