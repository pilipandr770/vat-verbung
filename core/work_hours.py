"""
Work Hours Manager - ensures notifications only during business hours.
Prevents notifications from bothering users during night time.

Supports:
- Day/Night mode scheduling (9:00-18:00 default)
- Time window validation for jobs
- Random delays between 3-5 minutes for natural behavior
"""

import logging
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class WorkHoursManager:
    """Manages work hours and time-based scheduling."""
    
    def __init__(self):
        """Initialize work hours manager."""
        self.work_hours_start = int(os.getenv("WORK_HOURS_START", "9"))
        self.work_hours_end = int(os.getenv("WORK_HOURS_END", "18"))
        self.timezone = os.getenv("TIMEZONE", "UTC")
        
        logger.info(f"Work hours: {self.work_hours_start}:00 - {self.work_hours_end}:00 {self.timezone}")
    
    def is_work_hours(self, check_time: datetime = None) -> bool:
        """
        Check if current time is within work hours.
        
        Args:
            check_time: Time to check (default: now)
            
        Returns:
            True if within work hours, False otherwise
        """
        if check_time is None:
            check_time = datetime.now()
        
        current_hour = check_time.hour
        is_working = self.work_hours_start <= current_hour < self.work_hours_end
        
        if not is_working:
            logger.debug(
                f"Outside work hours: {current_hour}:00 "
                f"(allowed: {self.work_hours_start}-{self.work_hours_end})"
            )
        
        return is_working
    
    def get_next_work_hour(self, check_time: datetime = None) -> datetime:
        """
        Get next work hour if outside work hours.
        
        Args:
            check_time: Time to check from (default: now)
            
        Returns:
            datetime of next work hour
        """
        if check_time is None:
            check_time = datetime.now()
        
        current_hour = check_time.hour
        
        if self.work_hours_start <= current_hour < self.work_hours_end:
            # Already in work hours
            return check_time
        
        if current_hour < self.work_hours_start:
            # Before work hours today
            return check_time.replace(hour=self.work_hours_start, minute=0, second=0)
        else:
            # After work hours, schedule for tomorrow
            from datetime import timedelta
            next_day = check_time + timedelta(days=1)
            return next_day.replace(hour=self.work_hours_start, minute=0, second=0)
    
    @staticmethod
    def random_delay(min_seconds: int = 180, max_seconds: int = 300) -> float:
        """
        Generate random delay between messages.
        Default: 3-5 minutes for natural behavior.
        
        Args:
            min_seconds: Minimum delay (default: 180 = 3 min)
            max_seconds: Maximum delay (default: 300 = 5 min)
            
        Returns:
            Random delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"Random delay: {delay:.1f} seconds ({delay/60:.1f} minutes)")
        return delay
    
    @staticmethod
    def random_delay_between_invites() -> float:
        """
        Get random delay between 3-5 minutes for invitations.
        
        Returns:
            Delay in seconds
        """
        return WorkHoursManager.random_delay(180, 300)
    
    @staticmethod
    def should_process_batch() -> bool:
        """
        Determine if invitation batch should proceed.
        Can be used to randomly skip some batches for natural behavior.
        
        Returns:
            True (can be overridden for A/B testing)
        """
        return True
    
    def get_work_hours_info(self) -> dict:
        """
        Get current work hours configuration.
        
        Returns:
            Dict with work hours info
        """
        now = datetime.now()
        
        return {
            "work_hours_start": self.work_hours_start,
            "work_hours_end": self.work_hours_end,
            "timezone": self.timezone,
            "current_hour": now.hour,
            "is_work_hours": self.is_work_hours(now),
            "next_work_hour": self.get_next_work_hour(now).isoformat(),
        }


class PublicationScheduler:
    """Handles publication timing during work hours."""
    
    # Default publication times during work hours (9:00-18:00)
    INSTAGRAM_TIMES = [(9, 0), (13, 0), (17, 0)]      # 3 times during work hours
    TELEGRAM_TIMES = [(9, 30), (12, 0), (15, 0), (17, 30)]  # 4 times during work hours
    LINKEDIN_TIMES = [(10, 0), (15, 0)]               # 2 times during work hours
    
    def __init__(self):
        """Initialize publication scheduler."""
        self.work_hours = WorkHoursManager()
    
    def get_instagram_times(self) -> list:
        """Get Instagram publication times (3 per day, 9-18)."""
        return self.INSTAGRAM_TIMES
    
    def get_telegram_times(self) -> list:
        """Get Telegram publication times (4 per day, 9-18)."""
        return self.TELEGRAM_TIMES
    
    def get_linkedin_times(self) -> list:
        """Get LinkedIn publication times (2 per day, 9-18)."""
        return self.LINKEDIN_TIMES
    
    def all_times_in_work_hours(self) -> bool:
        """Verify all scheduled times are within work hours."""
        all_times = self.INSTAGRAM_TIMES + self.TELEGRAM_TIMES + self.LINKEDIN_TIMES
        
        for hour, minute in all_times:
            if not (self.work_hours.work_hours_start <= hour < self.work_hours.work_hours_end):
                return False
        
        return True
