#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI Content Generator
Generates B2B marketing content using OpenAI (GPT) or Google Gemini APIs
"""

import os
import logging
from typing import Tuple, Dict, Optional
from enum import Enum
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class ContentTopic(str, Enum):
    """Content topics focused on VAT-Verifizierung Business Intelligence Platform"""
    COMPLIANCE = "compliance"           # VAT verification, regulations, compliance risk
    BUSINESS_INTELLIGENCE = "bi"       # OSINT analysis, data-driven insights
    VERIFICATION = "verification"     # Partner verification, validation, trust building
    INTEGRATION = "integration"       # API integration, automation, workflows
    SECURITY = "security"             # Link scanning, malware detection, threat prevention
    EFFICIENCY = "efficiency"         # Cost reduction, time savings, ROI
    TRUST = "trust"                   # Transparency, compliance confidence, reliability
    DATA_QUALITY = "data_quality"     # Data accuracy, CRM features, business profiles

class ContentType(str, Enum):
    """Types of content"""
    PAIN = "pain"               # Problem/pain point
    WARNING = "warning"         # Risk/warning
    USE_CASE = "use_case"      # Real example
    EXPLANATION = "explanation" # Educational

class AIProvider:
    """OpenAI provider"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
        self.client = None
        
        if not self.api_key:
            logger.warning("⚠️  OPENAI_API_KEY not configured")
            return
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"✅ OpenAI client initialized (model: {self.model})")
        except ImportError:
            logger.error("❌ openai library not installed: pip install openai")
            self.client = None
    
    def generate_content(
        self, 
        topic: ContentTopic, 
        content_type: ContentType,
        target_audience: str = "B2B managers in Germany"
    ) -> Tuple[str, ContentTopic, ContentType]:
        """
        Generate content using OpenAI GPT
        
        Args:
            topic: Content topic
            content_type: Type of content
            target_audience: Target audience description
            
        Returns:
            Tuple of (generated_text, topic, content_type)
        """
        if not self.client:
            logger.error("❌ OpenAI client not initialized")
            return None
        
        prompt = self._create_prompt(topic, content_type, target_audience)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional B2B marketing content writer. Create engaging, professional German B2B content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            content = response.choices[0].message.content.strip()
            logger.info(f"✅ Generated {content_type.value} content on {topic.value}")
            return (content, topic, content_type)
            
        except Exception as e:
            logger.error(f"❌ Error generating content: {str(e)}")
            return None
    
    def _create_prompt(self, topic: ContentTopic, content_type: ContentType, audience: str) -> str:
        """Create VAT-Verifizierung focused prompts for content generation"""
        
        base = f"You are a professional B2B marketing content writer for {audience}. Write in German. "
        base += f"Focus on VAT-Verifizierung (vat-verifizierung.de) - a Business Intelligence Platform. "
        base += f"Mention features like VIES validation, sanctions screening, OSINT scanner, link scanner, "
        base += f"MailGuard AI, Smart CRM, website security, compliance, and API integration. "
        base += f"Keep it concise, 1 paragraph, professional, engaging. Include pricing plans (Basierend €9.99, Professional €49.99, Enterprise €149.99). "
        base += f"IMPORTANT: End with ONE strong call-to-action (CTA) like 'Jetzt kostenlos testen auf vat-verifizierung.de', 'Demo vereinbaren', or 'Mehr erfahren'. Include the website link ONLY ONCE in the CTA.\n\n"
        
        prompts = {
            (ContentTopic.COMPLIANCE, ContentType.PAIN): 
                base + "Write about compliance risks in B2B: VAT verification, sanctions list risks, regulatory fines. "
                "Show pain of manual processes. Mention VIES validation and automated screening. Make it urgent.",
            
            (ContentTopic.COMPLIANCE, ContentType.WARNING):
                base + "Write a warning about GDPR compliance, VAT fraud risks, and sanctions list exposure. "
                "Emphasize that compliance automation is not optional. Mention EU, OFAC, UK sanctions lists.",
            
            (ContentTopic.COMPLIANCE, ContentType.USE_CASE):
                base + "Write a case study: How a company avoided €250K compliance fine through automated VAT verification. "
                "Show VIES validation, sanctions screening, real results. Be specific with numbers.",
            
            (ContentTopic.COMPLIANCE, ContentType.EXPLANATION):
                base + "Explain VIES validation, sanctions list screening, and compliance automation. "
                "Educational tone. Describe what EU, OFAC, UK sanctions are. Why real-time validation matters.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.PAIN):
                base + "Write about missing business intelligence: OSINT gaps, domain analysis blindness, partner risk unknown. "
                "Show cost of failed due diligence. Mention fraud prevention.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.WARNING):
                base + "Write about competitors using OSINT for intelligence gathering. "
                "Warn about link scanning risks, phishing masquerades, website security gaps. "
                "Show what hackers can discover about your partners.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.USE_CASE):
                base + "Write case study: OSINT scanner discovered fake business before partnership. "
                "Domain analysis revealed phishing attempt. DNS records exposed threats.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.EXPLANATION):
                base + "Explain OSINT for B2B: domain analysis, DNS records, SSL certificates, WHOIS, social media. "
                "Educational. Link scanner integration with VirusTotal and Google Safe Browsing.",
            
            (ContentTopic.VERIFICATION, ContentType.PAIN):
                base + "Write about partner verification nightmare: manual checks, handelsregister lookups, insolvency risks. "
                "Show time waste - 60 seconds per partner × 1000 partners. Firmenprofil auto-fill saves time.",
            
            (ContentTopic.VERIFICATION, ContentType.WARNING):
                base + "Write: Ghost companies and false identities cost millions. Handelsregister verification essential. "
                "Smart CRM prevents bad partnerships. Auto-matching improves accuracy.",
            
            (ContentTopic.VERIFICATION, ContentType.USE_CASE):
                base + "Case study: Manufacturing company verified 1000 partners in 1 week with Smart CRM. "
                "Firmenprofil auto-fill saved 60 seconds per partner. Complete verification history.",
            
            (ContentTopic.VERIFICATION, ContentType.EXPLANATION):
                base + "Explain partner verification process: handelsregister checks, company profiles, due diligence. "
                "How Smart CRM + Firmenprofil automates partner management. Insolvency checking benefits.",
            
            (ContentTopic.INTEGRATION, ContentType.PAIN):
                base + "Write: Isolated verification systems waste time. Manual data entry. APIs missing. "
                "No workflow automation. REST API integration solves this. White-label solutions for partners.",
            
            (ContentTopic.INTEGRATION, ContentType.WARNING):
                base + "Write: Companies without API integration fall behind. Workflow automation is competitive advantage. "
                "White-label solutions matter for enterprise customers. Custom integration is differentiator.",
            
            (ContentTopic.INTEGRATION, ContentType.USE_CASE):
                base + "Case study: ERP + REST API integration automated partner verification. "
                "Automatic approval workflow. White-label solution for reseller partners.",
            
            (ContentTopic.INTEGRATION, ContentType.EXPLANATION):
                base + "Explain REST API integration benefits for workflows. White-label solutions explained. "
                "How automation connects VIES, sanctions, CRM. Enterprise API options.",
            
            (ContentTopic.SECURITY, ContentType.PAIN):
                base + "Write: Phishing links in B2B emails. Malware risks. Website security unknown. "
                "MailGuard AI + Link Scanner solves this. Gmail/Outlook integration automatic.",
            
            (ContentTopic.SECURITY, ContentType.WARNING):
                base + "Write: 40% of business compromises from links. Website security critical. "
                "Link scanning non-negotiable. MailGuard AI protects email. Website security checks essential.",
            
            (ContentTopic.SECURITY, ContentType.USE_CASE):
                base + "Case study: MailGuard AI blocked phishing campaign targeting company. "
                "Link scanner detected malware before clicks. Website security audit found 5 vulnerabilities.",
            
            (ContentTopic.SECURITY, ContentType.EXPLANATION):
                base + "Explain link scanning (VirusTotal, Google Safe Browsing). MailGuard AI with ML. "
                "Website security: SSL/TLS, security headers, vulnerability checks. AI recommendations.",
            
            (ContentTopic.EFFICIENCY, ContentType.PAIN):
                base + "Write: Manual verification costs €5-10 per partner. Scales inefficiently. "
                "Time waste: 60 seconds × 100 partners = 10+ hours/month. Basierend plan (€9.99) with 100 checks/month saves costs.",
            
            (ContentTopic.EFFICIENCY, ContentType.WARNING):
                base + "Write: Automation or manual chaos. Professional plan (€49.99, 500 checks/month) needed for scaling. "
                "Enterprise plan unlimited. 3 days free trial shows immediate ROI.",
            
            (ContentTopic.EFFICIENCY, ContentType.USE_CASE):
                base + "Case study: Company reduced verification costs from €1000/month to €49.99 Professional plan. "
                "Time savings: 100 hours/month to 5 hours. Unlimited Enterprise option.",
            
            (ContentTopic.EFFICIENCY, ContentType.EXPLANATION):
                base + "Explain tariff plans: Basierend (€9.99), Professional (€49.99), Enterprise (€149.99 unlimited). "
                "ROI calculation for automation. How pricing scales with business needs.",
            
            (ContentTopic.TRUST, ContentType.PAIN):
                base + "Write: Trusting partners without facts. DSGVO compliance concerns. Audit trails missing. "
                "Monitoring gaps. Complete verification history matters for confidence.",
            
            (ContentTopic.TRUST, ContentType.WARNING):
                base + "Write: DSGVO-compliant storage critical. Monitoring & alerts non-negotiable. "
                "Verlauf & Berichte for compliance. Transparency builds trust. Render.com hosting secure.",
            
            (ContentTopic.TRUST, ContentType.USE_CASE):
                base + "Case study: Company achieved GDPR compliance with Verlauf & Berichte export. "
                "Monitoring alerts notified changes immediately. Audit trails satisfied regulators.",
            
            (ContentTopic.TRUST, ContentType.EXPLANATION):
                base + "Explain GDPR compliance for data processors. Verlauf & Berichte documentation. "
                "Monitoring & alerts for partner status changes. Complete audit trails. Render.com hosting.",
            
            (ContentTopic.DATA_QUALITY, ContentType.PAIN):
                base + "Write: CRM data 30% wrong. Firmenprofil chaos. Historische Prüfungen lost. "
                "Smart CRM auto-saves. KI-Assistent organizes. Auto-fill saves 60 seconds per check.",
            
            (ContentTopic.DATA_QUALITY, ContentType.WARNING):
                base + "Write: Bad data costs money. CRM without structure fails. Prüfungshistorie critical. "
                "Smart CRM with tags and notes. KI-Assistent for navigation. Data quality is foundation.",
            
            (ContentTopic.DATA_QUALITY, ContentType.USE_CASE):
                base + "Case study: Firmenprofil auto-fill saves 60 seconds × 1000 partners = 280 hours/year. "
                "Smart CRM stores 1000+ contacts with complete history. KI-Assistent handles 500+ questions/month.",
            
            (ContentTopic.DATA_QUALITY, ContentType.EXPLANATION):
                base + "Explain Smart CRM features: auto-save, tags, notes. Firmenprofil reusability. "
                "KI-Assistent for 24/7 support. Data quality = better decisions. CRM capabilities.",
        }
        
        return prompts.get((topic, content_type), base + "Write engaging content about business verification and compliance.")

class GeminiProvider:
    """Google Gemini provider"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = os.getenv('AI_MODEL', 'gemini-pro')
        
        if not self.api_key:
            logger.warning("⚠️  GEMINI_API_KEY not configured")
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            logger.info(f"✅ Gemini client initialized (model: {self.model})")
        except ImportError:
            logger.error("❌ google-generativeai library not installed: pip install google-generativeai")
            self.client = None
    
    def generate_content(
        self,
        topic: ContentTopic,
        content_type: ContentType,
        target_audience: str = "B2B managers in Germany"
    ) -> Tuple[str, ContentTopic, ContentType]:
        """Generate content using Google Gemini"""
        
        if not self.client:
            logger.error("❌ Gemini client not initialized")
            return None
        
        prompt = self._create_prompt(topic, content_type, target_audience)
        
        try:
            response = self.client.generate_content(prompt)
            content = response.text.strip()
            logger.info(f"✅ Generated {content_type.value} content on {topic.value} (Gemini)")
            return (content, topic, content_type)
            
        except Exception as e:
            logger.error(f"❌ Error generating content with Gemini: {str(e)}")
            return None
    
    def _create_prompt(self, topic: ContentTopic, content_type: ContentType, audience: str) -> str:
        """Create VAT-Verifizierung focused prompts for Gemini"""
        base = f"You are a professional B2B marketing writer for {audience}. Write in German. "
        base += f"Focus on VAT-Verifizierung - Business Intelligence Platform (vat-verifizierung.de). "
        base += f"Include platform features: VIES validation, sanctions screening, OSINT scanner, link scanner, "
        base += f"MailGuard AI, Smart CRM, Firmenprofil, website security, API integration, monitoring, compliance. "
        base += f"Mention pricing: Basierend €9.99 (100 checks), Professional €49.99 (500 checks), Enterprise €149.99 (unlimited). "
        base += f"Write 2-3 paragraphs, professional, engaging. Include 3 days free trial offer. "
        base += f"IMPORTANT: End with a strong call-to-action (CTA) like 'Jetzt kostenlos testen', 'Terminieren Sie eine Demo', 'Mehr erfahren' or 'Kontaktieren Sie uns'. Always include vat-verifizierung.de link.\n\n"
        
        prompts = {
            (ContentTopic.COMPLIANCE, ContentType.PAIN): 
                base + "Write about VAT verification pain: VIES validation risks, sanctions list exposure, "
                "compliance fines (€250K+), manual checking overhead. Show urgency.",
            
            (ContentTopic.COMPLIANCE, ContentType.WARNING):
                base + "Write warning: GDPR compliance mandatory, VAT fraud risks real, sanctions lists critical. "
                "Mention EU, OFAC, UK sanctions. Compliance automation non-negotiable.",
            
            (ContentTopic.COMPLIANCE, ContentType.USE_CASE):
                base + "Write case: Company avoided €250K fine through automated VIES validation and sanctions screening. "
                "Specific numbers. Real impact.",
            
            (ContentTopic.COMPLIANCE, ContentType.EXPLANATION):
                base + "Explain VIES validation process, sanctions list screening (EU/OFAC/UK), "
                "compliance automation benefits. Educational. Why real-time validation critical.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.PAIN):
                base + "Write: Missing business intelligence - no OSINT insights, domain analysis gaps, "
                "partner risks unknown. Failed due diligence costs millions.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.WARNING):
                base + "Write: Competitors using OSINT intelligence. Link scanning shows phishing risks. "
                "Website security unknown. Hackers mapping your partner network.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.USE_CASE):
                base + "Case: OSINT scanner revealed fake business before costly partnership. "
                "Domain analysis exposed phishing threat. DNS records found vulnerabilities.",
            
            (ContentTopic.BUSINESS_INTELLIGENCE, ContentType.EXPLANATION):
                base + "Explain OSINT for B2B: domain analysis, DNS records, SSL certificates, WHOIS lookups, "
                "social media presence. Link scanner with VirusTotal integration.",
            
            (ContentTopic.VERIFICATION, ContentType.PAIN):
                base + "Write: Partner verification nightmare - manual handelsregister checks, "
                "60 seconds per partner, insolvency risks, ghost companies. Firmenprofil auto-fill solves.",
            
            (ContentTopic.VERIFICATION, ContentType.WARNING):
                base + "Write: Ghost companies cost millions. Handelsregister verification essential. "
                "Bad partnerships destroy profitability. Smart CRM prevents disasters.",
            
            (ContentTopic.VERIFICATION, ContentType.USE_CASE):
                base + "Case: Manufacturer verified 1000 partners in 1 week with Smart CRM. "
                "Firmenprofil auto-fill saved 60 seconds each. Complete verification history.",
            
            (ContentTopic.VERIFICATION, ContentType.EXPLANATION):
                base + "Explain partner verification: handelsregister, company profiles, due diligence process. "
                "How Smart CRM + Firmenprofil automate partner management.",
            
            (ContentTopic.INTEGRATION, ContentType.PAIN):
                base + "Write: Isolated verification systems waste time. Manual data entry. No API integration. "
                "Workflow automation missing. REST API solves integration problems.",
            
            (ContentTopic.INTEGRATION, ContentType.WARNING):
                base + "Write: Companies without API integration lose competitive advantage. "
                "Workflow automation critical for scaling. White-label solutions for partners.",
            
            (ContentTopic.INTEGRATION, ContentType.USE_CASE):
                base + "Case: ERP + REST API integration automated partner verification and approval workflow. "
                "White-label solution for reseller partners. Complete automation.",
            
            (ContentTopic.INTEGRATION, ContentType.EXPLANATION):
                base + "Explain REST API integration benefits, workflow automation possibilities, "
                "white-label solutions for partners. Enterprise API options.",
            
            (ContentTopic.SECURITY, ContentType.PAIN):
                base + "Write: Phishing links in B2B emails. Malware risks. Website security unknown. "
                "MailGuard AI and Link Scanner solve. Gmail/Outlook integration automatic.",
            
            (ContentTopic.SECURITY, ContentType.WARNING):
                base + "Write: 40% of breaches from links. Website security critical. "
                "Link scanning non-optional. MailGuard AI protects. Website security audits essential.",
            
            (ContentTopic.SECURITY, ContentType.USE_CASE):
                base + "Case: MailGuard AI blocked phishing campaign. Link scanner detected malware. "
                "Website security audit found 5 critical vulnerabilities.",
            
            (ContentTopic.SECURITY, ContentType.EXPLANATION):
                base + "Explain link scanning technology, MailGuard AI with ML detection, "
                "website security checks (SSL, headers, vulnerabilities).",
            
            (ContentTopic.EFFICIENCY, ContentType.PAIN):
                base + "Write: Manual verification €5-10 per partner. Time waste: 60 seconds × 100 partners = 10+ hours/month. "
                "Basierend €9.99 plan saves costs significantly.",
            
            (ContentTopic.EFFICIENCY, ContentType.WARNING):
                base + "Write: Automation or chaos. Professional €49.99 (500 checks) for growth. "
                "Enterprise unlimited for enterprises. Immediate ROI proven.",
            
            (ContentTopic.EFFICIENCY, ContentType.USE_CASE):
                base + "Case: Reduced costs from €1000/month manual to €49.99 Professional plan. "
                "Time: 100 hours/month to 5 hours. Enterprise unlimited option available.",
            
            (ContentTopic.EFFICIENCY, ContentType.EXPLANATION):
                base + "Explain pricing: Basierend €9.99 (100/mo), Professional €49.99 (500/mo), "
                "Enterprise €149.99 (unlimited). ROI calculation. Scaling strategy.",
            
            (ContentTopic.TRUST, ContentType.PAIN):
                base + "Write: Trusting partners without facts. DSGVO concerns. Audit trails missing. "
                "Verification history critical for confidence.",
            
            (ContentTopic.TRUST, ContentType.WARNING):
                base + "Write: GDPR compliance mandatory. Monitoring & alerts non-negotiable. "
                "Verlauf & Berichte for compliance documentation. Transparency builds trust.",
            
            (ContentTopic.TRUST, ContentType.USE_CASE):
                base + "Case: Achieved GDPR compliance with Verlauf & Berichte export. "
                "Monitoring alerts notified changes immediately. Auditors satisfied.",
            
            (ContentTopic.TRUST, ContentType.EXPLANATION):
                base + "Explain GDPR data processor requirements, audit trail documentation, "
                "monitoring alerts, complete verification history.",
            
            (ContentTopic.DATA_QUALITY, ContentType.PAIN):
                base + "Write: CRM data 30% wrong. Firmenprofil scattered. History lost. "
                "Smart CRM auto-saves. KI-Assistent organizes. Auto-fill saves time.",
            
            (ContentTopic.DATA_QUALITY, ContentType.WARNING):
                base + "Write: Bad data costs millions. CRM without structure fails. "
                "History critical. Smart CRM with structure. KI-Assistent helps.",
            
            (ContentTopic.DATA_QUALITY, ContentType.USE_CASE):
                base + "Case: Firmenprofil auto-fill saves 60 seconds × 1000 = 280 hours/year. "
                "Smart CRM manages 1000+ with complete history. KI-Assistent 24/7.",
            
            (ContentTopic.DATA_QUALITY, ContentType.EXPLANATION):
                base + "Explain Smart CRM: auto-save features, tags, notes organization. "
                "Firmenprofil reusability benefits. KI-Assistent 24/7 support.",
        }
        
        return prompts.get((topic, content_type), base + "Write engaging content about VAT verification and business intelligence.")

class AIContentGenerator:
    """Main AI content generator - handles both OpenAI and Gemini"""
    
    def __init__(self):
        self.use_ai = os.getenv('USE_AI_CONTENT', 'False').lower() == 'true'
        self.provider_name = os.getenv('AI_PROVIDER', 'openai').lower()
        
        if self.use_ai:
            if self.provider_name == 'openai':
                self.provider = AIProvider()
            elif self.provider_name == 'gemini':
                self.provider = GeminiProvider()
            else:
                logger.error(f"❌ Unknown provider: {self.provider_name}")
                self.provider = None
        else:
            logger.info("ℹ️  AI content generation disabled (USE_AI_CONTENT=False)")
            self.provider = None
    
    def generate(
        self,
        topic: ContentTopic,
        content_type: ContentType,
        target_audience: str = "B2B managers in Germany"
    ) -> Optional[Tuple[str, ContentTopic, ContentType]]:
        """Generate AI content"""
        
        if not self.provider:
            return None
        
        return self.provider.generate_content(topic, content_type, target_audience)
    
    def is_enabled(self) -> bool:
        """Check if AI generation is enabled"""
        return self.use_ai and self.provider is not None

# Fallback static content for VAT-Verifizierung platform
STATIC_CONTENT_FALLBACK = {
    ContentTopic.COMPLIANCE: {
        ContentType.PAIN: [
            "VAT-Prüfung: Das Risiko, das jedes Unternehmen kennen sollte",
            "Sanktionslisten-Kontrolle: Warum 80% der Unternehmen unvorbereitet sind",
        ],
        ContentType.WARNING: [
            "VIES-Validierung: Nicht optional für EU-Geschäfte",
            "Sanktionsrisiken im B2B: Härtere Strafen ab 2026",
        ],
        ContentType.USE_CASE: [
            "Fallstudie: Wie ein Handelsunternehmen 250K€ Bußgelder sparte",
            "Compliance-Automatisierung: Von 15 Prüfungen/Tag auf 1500",
        ],
        ContentType.EXPLANATION: [
            "VIES-Prüfung verstehen: Ein Leitfaden für Unternehmen",
            "Sanktionslisten: EU, OFAC, UK - Was Sie kontrollieren müssen",
        ],
    },
}
