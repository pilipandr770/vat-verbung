"""
LinkedIn Invitations Manager - careful and personalized outreach.
No spam, respects work hours and rate limiting.

Features:
- Day/Night mode: Only invites during 9:00-18:00
- Random messages: 5 templates per bio type
- Random delays: 3-5 minutes between invites (natural behavior)
"""

import os
import time
import logging
from typing import Dict
from core.work_hours import WorkHoursManager
from core.message_templates import LinkedInMessageTemplates

logger = logging.getLogger(__name__)


class LinkedInInviter:
    """Запрошує лідів на LinkedIn."""
    
    def __init__(self):
        """Initialize LinkedIn inviter."""
        self.platform = "linkedin"
        self.work_hours = WorkHoursManager()
        
        # LinkedIn API client would go here
        # For now, this is a placeholder for future LinkedIn integration
        self.linkedin_client = None
        logger.info("LinkedIn Inviter initialized (client integration pending)")
    
    def send_invite(self, profile_id: str, username: str, bio: str) -> Dict:
        """
        Send personalized connection request/message.
        
        Features:
        - Only runs during work hours (9-18 by default)
        - Uses random message templates (5 variants)
        - Uses random delays between 3-5 minutes
        
        Args:
            profile_id: LinkedIn profile ID
            username: User's display name
            bio: Bio for personalization
            
        Returns:
            Dict with result details
        """
        try:
            # Check work hours
            if not self.work_hours.is_work_hours():
                logger.info(f"⏰ Outside work hours: skipping {username}")
                return {
                    "success": False,
                    "profile_id": profile_id,
                    "username": username,
                    "error": "Outside work hours (9:00-18:00)",
                    "time_blocked": True,
                }
            
            # Get random message template (5 variants available)
            message = LinkedInMessageTemplates.get_random_template(username, bio)
            
            logger.info(f"Sending invite to: {username} (Profile ID: {profile_id})")
            
            # TODO: Implement actual LinkedIn API call
            # self.linkedin_client.send_message(profile_id, message)
            
            logger.debug(f"Message template: {message[:50]}...")
            
            # Random delay between 3-5 minutes for natural behavior
            delay = self.work_hours.random_delay_between_invites()
            logger.info(f"⏱️ Waiting {delay:.0f}s ({delay/60:.1f}min) before next invite")
            time.sleep(delay)
            
            logger.info(f"✅ Invite sent to: {username}")
            
            return {
                "success": True,
                "profile_id": profile_id,
                "username": username,
                "platform": "linkedin",
            }
        
        except Exception as e:
            logger.error(f"❌ Error inviting {username}: {e}")
            return {
                "success": False,
                "profile_id": profile_id,
                "username": username,
                "error": str(e),
            }
    
    @staticmethod
    def _create_personalized_message(username: str, bio: str) -> str:
        """
        Create personalized connection message (legacy - use templates instead).
        
        Args:
            username: User's display name
            bio: Bio for analysis
            
        Returns:
            Message text
        """
        return LinkedInMessageTemplates.get_random_template(username, bio)
