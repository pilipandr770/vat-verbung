#!/usr/bin/env python3
"""
Auto-generate .env file from Render environment variables
Runs before main.py to ensure .env exists with all required settings
"""
import os
from pathlib import Path

def create_env_from_environment():
    """Generate .env file from environment variables"""
    env_path = Path(__file__).parent / ".env"
    
    # List of all required environment variables
    required_vars = [
        # Database
        "DATABASE_URL",
        "DB_SCHEMA",
        
        # LinkedIn
        "LINKEDIN_USERNAME",
        "LINKEDIN_PASSWORD",
        "LINKEDIN_COMPANY_ID",
        
        # Telegram
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHANNEL_ID",
        
        # Instagram
        "INSTAGRAM_USERNAME",
        "INSTAGRAM_PASSWORD",
        "INSTAGRAM_SESSION",
        
        # General
        "DEBUG",
        "LOG_LEVEL",
        "LOG_FILE",
        
        # Scheduler
        "SCHEDULER_ENABLED",
        "SCHEDULER_TIMEZONE",
        
        # Content
        "CONTENT_LANGUAGE",
        "MAX_LEADS_PER_JOB",
        "SCORE_THRESHOLD_INVITE",
        "SCORE_THRESHOLD_SAVE",
        "MAX_INVITES_PER_LEAD",
        "POST_RETENTION_DAYS",
        "CLEANUP_ENABLED",
        "CLEANUP_TIME",
        
        # AI APIs
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "DALLE_API_KEY",
        "AI_PROVIDER",
        "AI_MODEL",
        "IMAGE_MODEL",
        "USE_AI_CONTENT",
        
        # Work hours
        "WORK_HOURS_START",
        "WORK_HOURS_END",
        "TIMEZONE",
        "WORK_HOURS_ENABLED",
        
        # Publication schedules
        "INSTAGRAM_POSTS_PER_DAY",
        "TELEGRAM_POSTS_PER_DAY",
        "LINKEDIN_POSTS_PER_DAY",
        
        # Invitations
        "INVITATION_DELAY_MIN",
        "INVITATION_DELAY_MAX",
        "USE_RANDOM_MESSAGES",
        "MESSAGE_TEMPLATE_VARIANTS",
    ]
    
    # Read from environment
    env_content = []
    for var in required_vars:
        value = os.getenv(var, "")
        if value:
            env_content.append(f"{var}={value}")
        else:
            # Set default values for optional variables
            defaults = {
                "DEBUG": "False",
                "LOG_LEVEL": "INFO",
                "LOG_FILE": "logs/promotion_hub.log",
                "SCHEDULER_ENABLED": "True",
                "SCHEDULER_TIMEZONE": "Europe/Berlin",
                "CONTENT_LANGUAGE": "DE",
                "MAX_LEADS_PER_JOB": "50",
                "SCORE_THRESHOLD_INVITE": "0.6",
                "SCORE_THRESHOLD_SAVE": "0.3",
                "MAX_INVITES_PER_LEAD": "1",
                "POST_RETENTION_DAYS": "30",
                "CLEANUP_ENABLED": "True",
                "CLEANUP_TIME": "02:00",
                "AI_PROVIDER": "openai",
                "AI_MODEL": "gpt-3.5-turbo",
                "IMAGE_MODEL": "dall-e-3",
                "USE_AI_CONTENT": "True",
                "WORK_HOURS_START": "9",
                "WORK_HOURS_END": "18",
                "TIMEZONE": "Europe/Berlin",
                "WORK_HOURS_ENABLED": "True",
                "INSTAGRAM_POSTS_PER_DAY": "3",
                "TELEGRAM_POSTS_PER_DAY": "3",
                "LINKEDIN_POSTS_PER_DAY": "2",
                "INVITATION_DELAY_MIN": "180",
                "INVITATION_DELAY_MAX": "300",
                "USE_RANDOM_MESSAGES": "True",
                "MESSAGE_TEMPLATE_VARIANTS": "5",
                "DALLE_API_KEY": "",
            }
            if var in defaults:
                env_content.append(f"{var}={defaults[var]}")
    
    # Write .env file
    env_path.write_text("\n".join(env_content))
    print(f"✅ Generated .env file with {len(env_content)} variables")
    return env_path


if __name__ == "__main__":
    create_env_from_environment()
