"""
Invitation Message Templates - 5 variations per channel for randomization.

Each channel has 5 different message templates that are randomly selected.
This prevents repetitive messages and improves engagement rates.

Templates are personalized based on user's bio keywords.
"""

import logging
import random

logger = logging.getLogger(__name__)


class InstagramMessageTemplates:
    """5 message template variations for Instagram invitations."""
    
    # Template variants for different bio keywords
    MARKETING_TEMPLATES = [
        """Hi {name}! 👋

Noticed you're into marketing & growth strategies. 

We've been sharing insights on B2B automation, digital transformation, and operational efficiency. 

Would love to have you in the conversation! 🚀""",
        
        """Hey {name}! 👋

Your marketing focus caught my eye.

We're building a community focused on B2B solutions and business optimization. Check us out?

Connect! 💼""",
        
        """Hi {name}! 👋

Marketing professional here 🎯

We're discussing practical approaches to B2B growth and automation. Thought you might find it interesting.

Let's connect? 📈""",
        
        """Hey {name}! 👋

Love your focus on marketing excellence.

We share insights on digital transformation and B2B strategy. Worth exploring together?

Cheers! ✨""",
        
        """Hi {name}! 👋

Saw your marketing passion 🔥

We're creating resources for B2B professionals on automation and efficiency. You'd fit right in!

Connect? 🌟""",
    ]
    
    CEO_FOUNDER_TEMPLATES = [
        """Hi {name}! 👋

Impressive founder journey! 🚀

We're connecting entrepreneurs discussing B2B growth, automation, and scaling. Might be interesting for you.

Let's chat? 💡""",
        
        """Hey {name}! 👋

Founder/CEO, respect! 👏

Building a community of business leaders focused on operational efficiency and digital transformation.

Join us? 🎯""",
        
        """Hi {name}! 👋

Your entrepreneurial background is amazing.

We're exploring B2B solutions and business optimization with fellow founders. Your perspective would be valuable.

Connect! 🌟""",
        
        """Hey {name}! 👋

Leading the startup scene! 💼

We're discussing practical strategies for business growth and automation. Thought of you immediately.

Let's connect? 🚀""",
        
        """Hi {name}! 👋

CEO/Founder energy! 🔥

We share insights on B2B challenges and solutions. Your experience would add so much to our conversations.

Join? 💬""",
    ]
    
    CONSULTANT_TEMPLATES = [
        """Hi {name}! 👋

Consulting background - impressive! 💼

We're building a community of consultants and B2B professionals. Thought you'd be a great fit.

Connect? 🎯""",
        
        """Hey {name}! 👋

Your consulting expertise is noted! 👏

We discuss B2B optimization, digital transformation, and business solutions. Your insights would be valuable.

Join us? 📊""",
        
        """Hi {name}! 👋

Consultant here too 🤝

We're connecting industry professionals focused on business efficiency and growth. You'd definitely fit in!

Let's chat? 💡""",
        
        """Hey {name}! 👋

Consulting professional! 💼

We share practical approaches to B2B challenges. Your perspective would enhance our conversations significantly.

Interested? 🌟""",
        
        """Hi {name}! 👋

Love your consulting focus 📈

We're building a network around B2B solutions and business optimization. Your expertise would be gold!

Connect? 🚀""",
    ]
    
    GENERAL_TEMPLATES = [
        """Hi {name}! 👋

I noticed we share interests in B2B solutions.

We're discussing digital transformation and business automation. Would you be interested in connecting?

Best regards! 💼""",
        
        """Hey {name}! 👋

Your profile caught my attention.

We're a community focused on B2B growth and operational efficiency. Thought you might find our content valuable!

Connect? 🎯""",
        
        """Hi {name}! 👋

Interesting profile! 🔥

We share insights on B2B strategies and automation. Feel free to check out our content and let's chat!

Looking forward! 💡""",
        
        """Hey {name}! 👋

Let's connect! 🤝

We're building conversations around B2B solutions and business optimization. Your perspective would be great!

What do you think? 📊""",
        
        """Hi {name}! 👋

Similar interests spotted! 👏

We discuss practical B2B approaches and digital transformation. Would love to have you join our conversations.

Let's chat? 🌟""",
    ]
    
    @classmethod
    def get_random_template(cls, username: str, bio: str) -> str:
        """
        Select random template based on bio keywords.
        
        Args:
            username: User's display name
            bio: User's bio text
            
        Returns:
            Randomly selected message template
        """
        bio_lower = bio.lower()
        
        # Check for CEO/Founder keywords first (highest priority)
        if any(kw in bio_lower for kw in ["ceo", "founder", "entrepreneur", "startup"]):
            template = random.choice(cls.CEO_FOUNDER_TEMPLATES)
            logger.debug(f"Selected CEO/Founder template for {username}")
        
        # Check for consultant keywords
        elif any(kw in bio_lower for kw in ["consulting", "consultant", "advisor"]):
            template = random.choice(cls.CONSULTANT_TEMPLATES)
            logger.debug(f"Selected Consultant template for {username}")
        
        # Check for marketing keywords
        elif any(kw in bio_lower for kw in ["marketing", "growth", "digital", "sales"]):
            template = random.choice(cls.MARKETING_TEMPLATES)
            logger.debug(f"Selected Marketing template for {username}")
        
        # Default to general templates
        else:
            template = random.choice(cls.GENERAL_TEMPLATES)
            logger.debug(f"Selected General template for {username}")
        
        return template.format(name=username)


class TelegramMessageTemplates:
    """5 message template variations for Telegram invitations."""
    
    MARKETING_TEMPLATES = [
        """👋 Hi {name}!

I noticed your interest in marketing & business growth.

We're sharing insights on B2B automation, digital transformation, and operational efficiency in our community.

Would you be interested in joining? 🚀""",
        
        """Hey {name}! 👋

Your marketing focus caught my attention.

We have a group discussing practical B2B solutions and business optimization. You'd fit perfectly!

Join us? 💼""",
        
        """Hi {name}! 👋

Marketing professional here 🎯

We're discussing effective B2B strategies and automation. Thought your expertise would be valuable to our conversations.

Interested? 📈""",
        
        """Hey {name}! 👋

Love your marketing insights!

We're building a community focused on B2B growth and digital transformation. Your perspective would be amazing.

Let's chat? ✨""",
        
        """Hi {name}! 👋

Saw your marketing passion 🔥

We're connecting B2B professionals to discuss growth strategies and automation. You'd be a great addition!

Join? 🌟""",
    ]
    
    CEO_FOUNDER_TEMPLATES = [
        """Hi {name}! 👋

Impressive founder/CEO background! 🚀

We're a community of entrepreneurs discussing B2B growth, automation, and scaling strategies.

Worth exploring? 💡""",
        
        """Hey {name}! 👋

Founder energy! 👏

We connect business leaders discussing operational efficiency and digital transformation. You'd fit right in!

Join us? 🎯""",
        
        """Hi {name}! 👋

Your entrepreneurial story is amazing.

We have a group of founders discussing B2B solutions and business optimization. Your insights would be invaluable.

Connect? 🌟""",
        
        """Hey {name}! 👋

Leading the business world! 💼

We discuss practical strategies for B2B growth and automation. Thought your perspective would be perfect for our discussions.

Let's connect? 🚀""",
        
        """Hi {name}! 👋

CEO/Founder perspective needed! 🔥

We're building a network of business leaders focused on automation and efficiency. Join us?

Cheers! 💬""",
    ]
    
    CONSULTANT_TEMPLATES = [
        """Hi {name}! 👋

Consulting background - impressed! 💼

We have a community of consultants and B2B professionals. Great fit for you!

Want to join? 🎯""",
        
        """Hey {name}! 👋

Your consulting expertise is valuable! 👏

We discuss B2B optimization and digital transformation. Your insights would enhance our conversations.

Interested? 📊""",
        
        """Hi {name}! 👋

Consultant here too 🤝

We're connecting industry experts focused on business efficiency. You'd definitely be a great addition!

Let's chat? 💡""",
        
        """Hey {name}! 👋

Consulting professional! 💼

We share practical approaches to B2B challenges. Your perspective would be incredibly valuable.

Join us? 🌟""",
        
        """Hi {name}! 👋

Love your consulting approach 📈

We're building a network around B2B solutions and optimization. Your expertise would be gold!

Connect? 🚀""",
    ]
    
    GENERAL_TEMPLATES = [
        """Hi {name}! 👋

I noticed we share interests in B2B solutions.

We have a group discussing digital transformation and business automation. Would you like to join our conversations?

Let's connect! 💼""",
        
        """Hey {name}! 👋

Your profile interests me!

We're a community focused on B2B growth and operational efficiency. You might find our content valuable!

Join? 🎯""",
        
        """Hi {name}! 👋

Interesting background! 🔥

We discuss B2B strategies and automation. Feel free to join our group and let's chat!

Looking forward! 💡""",
        
        """Hey {name}! 👋

Let's connect! 🤝

We're building conversations around B2B solutions and business optimization. Your perspective would be great!

Interested? 📊""",
        
        """Hi {name}! 👋

Similar interests spotted! 👏

We discuss practical B2B approaches. Would love to have you join our community.

What do you think? 🌟""",
    ]
    
    @classmethod
    def get_random_template(cls, username: str, bio: str) -> str:
        """
        Select random template based on bio keywords.
        
        Args:
            username: User's display name
            bio: User's bio text
            
        Returns:
            Randomly selected message template
        """
        bio_lower = bio.lower()
        
        if any(kw in bio_lower for kw in ["ceo", "founder", "entrepreneur", "startup"]):
            template = random.choice(cls.CEO_FOUNDER_TEMPLATES)
            logger.debug(f"Selected CEO/Founder template for {username}")
        
        elif any(kw in bio_lower for kw in ["consulting", "consultant", "advisor"]):
            template = random.choice(cls.CONSULTANT_TEMPLATES)
            logger.debug(f"Selected Consultant template for {username}")
        
        elif any(kw in bio_lower for kw in ["marketing", "growth", "digital", "sales"]):
            template = random.choice(cls.MARKETING_TEMPLATES)
            logger.debug(f"Selected Marketing template for {username}")
        
        else:
            template = random.choice(cls.GENERAL_TEMPLATES)
            logger.debug(f"Selected General template for {username}")
        
        return template.format(name=username)


class LinkedInMessageTemplates:
    """5 message template variations for LinkedIn invitations."""
    
    MARKETING_TEMPLATES = [
        """Hi {name},

I've noticed your focus on marketing and business growth. 

We're building a community discussing B2B automation, digital transformation, and operational efficiency.

Would be great to connect and share insights!

Best regards""",
        
        """Hi {name},

Your marketing expertise caught my attention.

We discuss practical B2B solutions and growth strategies. Your perspective would be valuable.

Let's connect!""",
        
        """Hi {name},

Marketing professional here. Saw your profile.

We're focused on B2B strategy and automation. Thought we might have synergies worth exploring.

Looking forward to connecting!""",
        
        """Hi {name},

Your marketing insights are impressive!

We have a professional community discussing B2B growth and digital transformation.

Would you be interested in connecting?""",
        
        """Hi {name},

Noticed your passion for marketing excellence.

We're connecting B2B professionals focused on innovation and efficiency. Valuable discussions happening.

Let's chat!""",
    ]
    
    CEO_FOUNDER_TEMPLATES = [
        """Hi {name},

Impressive founder/CEO background!

We're connecting entrepreneurs discussing B2B growth, scaling, and business optimization.

Would love to stay connected and exchange ideas!

Best regards""",
        
        """Hi {name},

Love what you're building as a founder!

We have a community of business leaders focused on B2B solutions and efficiency. Your perspective would be valuable.

Let's connect!""",
        
        """Hi {name},

Entrepreneur here too!

We discuss practical strategies for business growth and digital transformation. Would be great to connect.

Looking forward!""",
        
        """Hi {name},

Your entrepreneurial journey is impressive!

We're a network of founders discussing B2B challenges and solutions. Worth exploring together?

Let's stay connected!""",
        
        """Hi {name},

CEO perspective welcomed!

We're building conversations around B2B innovation and business optimization. Your insights would be gold.

Interested in connecting?""",
    ]
    
    CONSULTANT_TEMPLATES = [
        """Hi {name},

Consulting background - impressive work!

We have a professional community discussing B2B solutions and optimization. Perfect fit for you.

Let's connect!""",
        
        """Hi {name},

Your consulting expertise is noted.

We discuss B2B challenges and digital transformation. Your insights would enhance our professional network.

Interested in connecting?""",
        
        """Hi {name},

Consultant here as well.

We're connecting industry experts focused on business efficiency. Would love to have you in our network!

Let's chat!""",
        
        """Hi {name},

Consulting professional - great to see!

We share practical approaches to B2B solutions. Your perspective would be very valuable to us.

Let's connect!""",
        
        """Hi {name},

Love your consulting approach!

We're building a professional network around B2B optimization. Your expertise would be incredible.

Looking forward to connecting!""",
    ]
    
    GENERAL_TEMPLATES = [
        """Hi {name},

I noticed we share interests in B2B solutions.

We're a professional community discussing digital transformation and business optimization.

Would be great to stay connected!""",
        
        """Hi {name},

Your profile interests me!

We're focused on B2B growth and operational efficiency. Your perspective would be valuable.

Let's connect!""",
        
        """Hi {name},

Great background in your field!

We discuss B2B strategy and automation. Thought we might have interesting conversations.

Looking forward to connecting!""",
        
        """Hi {name},

Saw your professional profile!

We're a community focused on B2B solutions and efficiency. Would love to have you connected.

What do you think?""",
        
        """Hi {name},

Similar professional interests spotted!

We discuss practical B2B approaches and innovation. Would be great to expand our network with you.

Let's stay connected!""",
    ]
    
    @classmethod
    def get_random_template(cls, username: str, bio: str) -> str:
        """
        Select random template based on bio keywords.
        
        Args:
            username: User's display name
            bio: User's bio text
            
        Returns:
            Randomly selected message template
        """
        bio_lower = bio.lower()
        
        if any(kw in bio_lower for kw in ["ceo", "founder", "entrepreneur", "startup", "owner"]):
            template = random.choice(cls.CEO_FOUNDER_TEMPLATES)
            logger.debug(f"Selected CEO/Founder template for {username}")
        
        elif any(kw in bio_lower for kw in ["consulting", "consultant", "advisor", "coach"]):
            template = random.choice(cls.CONSULTANT_TEMPLATES)
            logger.debug(f"Selected Consultant template for {username}")
        
        elif any(kw in bio_lower for kw in ["marketing", "growth", "digital", "sales", "business development"]):
            template = random.choice(cls.MARKETING_TEMPLATES)
            logger.debug(f"Selected Marketing template for {username}")
        
        else:
            template = random.choice(cls.GENERAL_TEMPLATES)
            logger.debug(f"Selected General template for {username}")
        
        return template.format(name=username)


def get_random_message(channel: str, username: str, bio: str) -> str:
    """
    Get random message template for specified channel.
    
    Args:
        channel: "instagram", "telegram", or "linkedin"
        username: User's display name
        bio: User's bio text
        
    Returns:
        Randomly selected and formatted message
    """
    if channel.lower() == "instagram":
        return InstagramMessageTemplates.get_random_template(username, bio)
    elif channel.lower() == "telegram":
        return TelegramMessageTemplates.get_random_template(username, bio)
    elif channel.lower() == "linkedin":
        return LinkedInMessageTemplates.get_random_template(username, bio)
    else:
        logger.warning(f"Unknown channel: {channel}, using general template")
        return InstagramMessageTemplates.get_random_template(username, bio)
