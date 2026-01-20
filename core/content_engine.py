"""
ЄДИНИЙ контент-завод.
Генерує B2B-контент німецькою мовою (DE) як AI-генерований, так і з fallback
по темах: ризики, довіра, автоматизація, операційка.

Контент має різні типи: pain (проблеми), warning (попередження),
use-case (прикладифоів), explanation (пояснення).

AI Integration: OpenAI (GPT) або Google Gemini для динамічної генерації
"""

import random
import logging
from typing import List, Dict, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ContentTopic(str, Enum):
    """Content topics focused on VAT-Verifizierung Business Intelligence Platform."""
    COMPLIANCE = "compliance"           # VAT verification, sanctions screening, regulations
    BUSINESS_INTELLIGENCE = "bi"       # OSINT, data analytics, business insights
    VERIFICATION = "verification"     # Partner verification, validation, trust
    INTEGRATION = "integration"       # API integration, automation, system connectivity
    SECURITY = "security"             # Link scanning, malware detection, website security
    EFFICIENCY = "efficiency"         # Cost reduction, time savings, process optimization
    TRUST = "trust"                   # Transparency, compliance confidence, reliability
    DATA_QUALITY = "data_quality"     # Data accuracy, CRM, complete business profiles


class ContentType(str, Enum):
    """Типи контенту."""
    PAIN = "pain"           # Проблема/больовий пункт
    WARNING = "warning"     # Попередження/ризик
    USE_CASE = "use_case"   # Приклад з реальної практики
    EXPLANATION = "explanation"  # Пояснення концепції


class ContentEngine:
    """Генератор B2B-контенту німецькою мовою з AI-підтримкою."""
    
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
        
        # Initialize AI generator
        try:
            from core.ai_content import AIContentGenerator
            self.ai_generator = AIContentGenerator()
            logger.info("✅ AI content generator initialized")
        except ImportError as e:
            logger.warning(f"⚠️  AI generator not available: {e}")
            self.ai_generator = None
        
        # Initialize image generator
        try:
            from core.image_generator import ImageGenerator, PlaceholderImageGenerator
            self.image_generator = ImageGenerator()
            self.placeholder_generator = PlaceholderImageGenerator()
            logger.info("✅ Image generator initialized")
        except ImportError as e:
            logger.warning(f"⚠️  Image generator not available: {e}")
            self.image_generator = None
            self.placeholder_generator = None
    
    def _init_content_library(self) -> Dict[ContentTopic, Dict[ContentType, List[str]]]:
        """Initialize content library focused on VAT-Verifizierung platform."""
        return {
            ContentTopic.COMPLIANCE: {
                ContentType.PAIN: [
                    "VAT-Prüfung: Das Risiko, das jedes Unternehmen kennen sollte",
                    "Sanktionslisten-Kontrolle: Warum 80% der Unternehmen unvorbereitet sind",
                    "Compliance-Bußgelder: Ein stilles Millionenrisiko in Ihrer Supply Chain",
                ],
                ContentType.WARNING: [
                    "VIES-Validierung: Nicht optional für EU-Geschäfte",
                    "Sanktionsrisiken im B2B: Härtere Strafen ab 2026",
                    "Compliance-Automatisierung oder manuelle Fehlerquoten: Die Wahl",
                ],
                ContentType.USE_CASE: [
                    "Fallstudie: Wie ein Handelsunternehmen 250K€ Bußgelder sparte",
                    "Compliance-Automatisierung: Von 15 Prüfungen/Tag auf 1500",
                    "Praktisches Beispiel: VIES-Validierung reduziert Fraud um 95%",
                ],
                ContentType.EXPLANATION: [
                    "VIES-Prüfung verstehen: Ein Leitfaden für Unternehmen",
                    "Sanktionslisten: EU, OFAC, UK - Was Sie kontrollieren müssen",
                    "Compliance-Automatisierung: Risiken minimieren, Effizienz erhöhen",
                ],
            },
            ContentTopic.BUSINESS_INTELLIGENCE: {
                ContentType.PAIN: [
                    "OSINT-Blindheit: Wer sind Ihre Geschäftspartner wirklich?",
                    "Fehlende Due Diligence: Ein Risiko von 2 Millionen Euro",
                    "Domain-Intelligence: Wie Konkurrenten Ihr Netzwerk analysieren",
                ],
                ContentType.WARNING: [
                    "OSINT-Scanner: Der Wettbewerbsnachteil, den Sie ignorieren",
                    "Link-Scanning: Phishing-Masken in Ihrem E-Mail-Posteingang",
                    "Website-Security: 60% der B2B-Webseiten haben kritische Lücken",
                ],
                ContentType.USE_CASE: [
                    "OSINT-Analyse: Wie ein Unternehmen Betrugsversuche frühzeitig erkannte",
                    "Smart CRM + OSINT: Von Datenchaos zur Intelligenz",
                    "Domain-Analyse: KI deckt versteckte Geschäftsbeziehungen auf",
                ],
                ContentType.EXPLANATION: [
                    "OSINT verstehen: Open Source Intelligence für B2B",
                    "Domain-Intelligence: DNS, SSL, WHOIS - Was Sie wissen sollten",
                    "KI-gestützte Business Insights: Ein neuer Standard",
                ],
            },
            ContentTopic.VERIFICATION: {
                ContentType.PAIN: [
                    "Partner-Verifizierung: Das zeitraubende Prozessalptraum",
                    "Handelsregister-Lücken: Wer sind die echten Unternehmenseigentümer?",
                    "Manuell Verifizierung: 60 Sekunden pro Partner, 100 Partner = Leid",
                ],
                ContentType.WARNING: [
                    "Verifizierungsbias: Falsche Partner kosten 2x mehr als richtige",
                    "Insolvenzblindheit: Geschäfte mit insolventen Unternehmen",
                    "Unternehmensidentität: Ghost Companies und versteckte Strukturen",
                ],
                ContentType.USE_CASE: [
                    "Partner-Verifizierung in 60 Sekunden statt 60 Minuten",
                    "Fallstudie: Auto-Matching mit Handelsregister spart 100 Stunden/Monat",
                    "Praktisches Beispiel: Smart CRM verifiziert 10.000 Partner automatisch",
                ],
                ContentType.EXPLANATION: [
                    "Geschäftspartner-Verifizierung: Ein Rahmenwerk",
                    "Firmenprofil-Matching: Wie Automatisierung Genauigkeit erhöht",
                    "Due Diligence digital: Best Practices für B2B",
                ],
            },
            ContentTopic.INTEGRATION: {
                ContentType.PAIN: [
                    "API-Integration: Der Hidden Cost von isolierten Daten",
                    "REST API vergessen: Ihre Systeme arbeiten nicht zusammen",
                    "Workflow-Silos: Manuelle Daten-Replikation in jedem System",
                ],
                ContentType.WARNING: [
                    "System-Integration: Die Grundlage für digitale Effizienz",
                    "Automatisierte APIs: Nicht-Verhandelbar für Enterprise",
                    "White-Label-Lösungen: Custom Integration ist dein Vorteil",
                ],
                ContentType.USE_CASE: [
                    "REST API Integration: Von 3 Systemen zu 1 Quelle",
                    "White-Label-Lösung: Partner-Plattform mit VAT-Verifizierung",
                    "Praktisches Beispiel: ERP + Verifizierung = Automatische Freigabe",
                ],
                ContentType.EXPLANATION: [
                    "REST API Fundamentals: Warum Plattformen APIs brauchen",
                    "White-Label vs. Integration: Chancen und Herausforderungen",
                    "Workflow-Automatisierung: APIs als Nervensystem",
                ],
            },
            ContentTopic.SECURITY: {
                ContentType.PAIN: [
                    "Link-Sicherheit: Sind Ihre Partner-Links legitim?",
                    "Malware-Blindheit: Phishing-Links in B2B-E-Mails",
                    "Website-Sicherheit: SSL, HTTPS - Aber ist das genug?",
                ],
                ContentType.WARNING: [
                    "Link-Scanner: Phishing schlägt B2B-Unternehmen häufig",
                    "Malware-Risiken: 40% der Business-Kompromisse durch Links",
                    "MailGuard AI: KI-Schutz für E-Mail-Sicherheit",
                ],
                ContentType.USE_CASE: [
                    "Link-Scanner stoppt Malware-Kampagne vor Klick",
                    "MailGuard AI + Gmail/Outlook: Automatische Phishing-Filterung",
                    "Website-Security: AI erkennt Schwachstellen in Sekunden",
                ],
                ContentType.EXPLANATION: [
                    "Link-Scanner verstehen: VirusTotal, Google Safe Browsing",
                    "MailGuard AI: E-Mail-Sicherheit mit künstlicher Intelligenz",
                    "Website-Security: 7 Checks für Business-Webseiten",
                ],
            },
            ContentTopic.EFFICIENCY: {
                ContentType.PAIN: [
                    "Manual Business Intelligence: 1000x ineffizienter als automatisiert",
                    "Zeit-Verschwendung: 60 Sekunden pro Partner = 10+ Stunden/Monat",
                    "Kosten-Explosion: Jede Prüfung kostet 5-10€ in Arbeitszeit",
                ],
                ContentType.WARNING: [
                    "Automatisierung: Nicht optional für Skalierung",
                    "3 Tage kostenlos testen: ROI wird sichtbar sofort",
                    "100 Prüfungen/Monat: Basierend-Plan vs. 500/Monat Professional",
                ],
                ContentType.USE_CASE: [
                    "Kostenreduktion: Von 1000€/Monat auf 50€ mit Automatisierung",
                    "Zeit-Einsparung: Von 100 Stunden auf 5 Stunden/Monat",
                    "Praktisches Beispiel: 500 Partner in 1 Woche verifiziert",
                ],
                ContentType.EXPLANATION: [
                    "Automatisierungs-ROI: Wie man Effizienz berechnet",
                    "Tarif-Planung: Basierend vs. Professional vs. Enterprise",
                    "Unbegrenzte Prüfungen: Enterprise-Plan für Skalierung",
                ],
            },
            ContentTopic.TRUST: {
                ContentType.PAIN: [
                    "Vertrauen in Partner ohne Fakten",
                    "DSGVO-Compliance: Wie speichert man Daten sicher?",
                    "Transparenz fehlt: Keine Audit-Trails für Prüfungen",
                ],
                ContentType.WARNING: [
                    "DSGVO-konform oder nicht: Das ist eine Compliance-Frage",
                    "Monitoring & Alerts: Nicht-Verhandelbar für Partnerverwaltung",
                    "Verlauf & Berichte: Compliance-Dokumentation ist Pflicht",
                ],
                ContentType.USE_CASE: [
                    "DSGVO-Compliance in Cloud: Render.com gehostet, sicher",
                    "Monitoring: Automatische Benachrichtigungen bei Statusänderungen",
                    "Audit-Trails: Vollständige Prüfungshistorie exportierbar",
                ],
                ContentType.EXPLANATION: [
                    "DSGVO in der Praxis: Was Datenverarbeiter beachten",
                    "Transparenz-Bericht: Compliance-Dokumentation verstehen",
                    "Trust-Building: Sicherheit, Transparenz, Automatisierung",
                ],
            },
            ContentTopic.DATA_QUALITY: {
                ContentType.PAIN: [
                    "Schlechte Datenqualität: 30% der CRM-Daten sind falsch",
                    "Firmenprofil-Chaos: Keine zentralen Unternehmenseigenschaften",
                    "Notizen verloren: Historische Prüfungen sind nicht nachverfolgbar",
                ],
                ContentType.WARNING: [
                    "Datenqualität: Der verborgene Kostenfaktor",
                    "CRM ohne Struktur: Notizen, Tags, aber keine Intelligenz",
                    "Prüfungshistorie: Verloren ohne System",
                ],
                ContentType.USE_CASE: [
                    "Firmenprofil Auto-Fill: 60 Sekunden pro Prüfung gespart",
                    "Smart CRM: 1000+ Kontakte mit kompletter Historie",
                    "KI-Assistent: Chatbot beantwortet Fragen 24/7",
                ],
                ContentType.EXPLANATION: [
                    "Smart CRM: Automatische Speicherung von Prüfungsresultaten",
                    "Firmenprofil: Wiederverwendbare Daten sparen Zeit",
                    "KI-Assistent: Chatbot für Navigation und Support",
                ],
            },
        }
    
    def generate_content(
        self,
        topic: ContentTopic = None,
        content_type: ContentType = None,
        style: str = "professional",
        use_ai: bool = True,
    ) -> Tuple[str, ContentTopic, ContentType]:
        """
        Генерує контент за темою й типом (AI або fallback).
        
        Args:
            topic: Тема контенту (якщо None, вибирається з ротації)
            content_type: Тип контенту (якщо None, вибирається з ротації)
            style: Стиль презентації (professional, casual)
            use_ai: Спробувати AI генерацію (fallback до hardcoded)
            
        Returns:
            (текст контенту, тема, тип, источник)
        """
        if topic is None:
            topic = self.get_random_topic()
        
        if content_type is None:
            content_type = self.get_random_content_type()
        
        # Try AI generation if available and enabled
        if use_ai and self.ai_generator and self.ai_generator.is_enabled():
            try:
                ai_result = self.ai_generator.generate(topic, content_type)
                if ai_result:
                    content, returned_topic, returned_type = ai_result
                    logger.info(f"✅ Generated content via AI ({topic.value}/{content_type.value})")
                    return (content, returned_topic, returned_type)
            except Exception as e:
                logger.warning(f"⚠️  AI generation failed, falling back: {e}")
        
        # Fallback to static content
        return self._get_static_content(topic, content_type)
    
    def _get_static_content(
        self,
        topic: ContentTopic,
        content_type: ContentType,
    ) -> Tuple[str, ContentTopic, ContentType]:
        """Get content from static library"""
        
        content_list = self.content_library.get(topic, {}).get(content_type, [])
        
        if not content_list:
            return (
                f"Content for {topic.value}/{content_type.value} is not available",
                topic,
                content_type,
            )
        
        content = random.choice(content_list)
        return content, topic, content_type
    
    def generate_image(
        self,
        topic: ContentTopic,
        content_type: ContentType,
        description: Optional[str] = None,
    ) -> Optional[str]:
        """
        Генерує зображення за темою й типом контенту.
        
        Args:
            topic: Тема контенту
            content_type: Тип контенту
            description: Додатковий опис
            
        Returns:
            Шлях до збереженого зображення або None
        """
        
        # Try DALL-E if available
        if self.image_generator and self.image_generator.is_enabled():
            try:
                image_path = self.image_generator.generate_image(
                    topic.value,
                    content_type.value,
                    description
                )
                if image_path:
                    return image_path
            except Exception as e:
                logger.warning(f"⚠️  DALL-E generation failed: {e}")
        
        # Fallback to placeholder
        if self.placeholder_generator:
            try:
                image_path = self.placeholder_generator.generate_placeholder(
                    topic.value,
                    content_type.value
                )
                return image_path
            except Exception as e:
                logger.warning(f"⚠️  Placeholder generation failed: {e}")
        
        logger.warning(f"⚠️  No image generator available for {topic.value}/{content_type.value}")
        return None
    
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
