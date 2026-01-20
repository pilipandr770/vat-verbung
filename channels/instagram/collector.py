"""
Збір ЦА:
підписники схожих акаунтів,
активні користувачі,
коментарі.
"""

import os
import logging
from typing import List, Dict, Optional
from instagrapi import Client

logger = logging.getLogger(__name__)


class InstagramCollector:
    """Збирає цільову аудиторію з Instagram."""
    
    def __init__(self):
        """Ініціалізація Instagram collector."""
        self.platform = "instagram"
        self.client = Client()
        
        # Завантаження облікових даних
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("INSTAGRAM_USERNAME та INSTAGRAM_PASSWORD мають бути встановлені")
        
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Аутентифікація на Instagram."""
        try:
            logger.info(f"Authenticating to Instagram as {self.username}...")
            self.client.login(self.username, self.password)
            logger.info("✅ Instagram authentication successful")
        except Exception as e:
            logger.error(f"❌ Instagram authentication failed: {e}")
            raise
    
    def collect_from_similar_accounts(self, account_usernames: List[str]) -> List[Dict]:
        """
        Збирає лідів з підписників схожих акаунтів.
        
        Args:
            account_usernames: Список username схожих акаунтів (B2B-орієнтовані)
            
        Returns:
            Список виявлених лідів
        """
        leads = []
        
        for account_username in account_usernames:
            try:
                logger.info(f"Collecting from account: {account_username}")
                
                # Отримання інформації про акаунт
                user = self.client.user_info_by_username(account_username)
                user_id = user.pk
                
                # Отримання підписників (обмеження: Instagram API дозволяє обмежену кількість)
                # Примітка: instagrapi має обмеження, тому беремо перших 100
                followers = self.client.user_followers(user_id, amount=100)
                
                for follower in followers:
                    lead = {
                        "platform": "instagram",
                        "identifier": follower.username,
                        "username": follower.username,
                        "user_id": follower.pk,
                        "bio": follower.biography or "",
                        "source": f"followers_of_{account_username}",
                        "follower_count": follower.follower_count or 0,
                        "following_count": follower.following_count or 0,
                        "is_private": follower.is_private,
                    }
                    leads.append(lead)
                    logger.debug(f"Collected lead: {follower.username}")
                
                logger.info(f"✅ Collected {len(followers)} followers from {account_username}")
            
            except Exception as e:
                logger.error(f"Error collecting from {account_username}: {e}")
                continue
        
        return leads
    
    def collect_from_comments(self, post_ids: List[str]) -> List[Dict]:
        """
        Збирає лідів з коментарів під постами.
        
        Args:
            post_ids: List of Instagram media IDs
            
        Returns:
            Список виявлених лідів
        """
        leads = []
        
        for post_id in post_ids:
            try:
                logger.info(f"Collecting from post: {post_id}")
                
                # Отримання коментарів до посту
                comments = self.client.media_comments(post_id, amount=50)
                
                for comment in comments:
                    user = comment.user
                    lead = {
                        "platform": "instagram",
                        "identifier": user.username,
                        "username": user.username,
                        "user_id": user.pk,
                        "bio": user.biography or "",
                        "source": f"comments_on_{post_id}",
                        "comment_text": comment.text,
                        "follower_count": user.follower_count or 0,
                        "is_private": user.is_private,
                    }
                    leads.append(lead)
                    logger.debug(f"Collected lead: {user.username}")
                
                logger.info(f"✅ Collected {len(comments)} commenters from post {post_id}")
            
            except Exception as e:
                logger.error(f"Error collecting from post {post_id}: {e}")
                continue
        
        return leads
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """
        Отримує детальну інформацію про користувача.
        
        Args:
            username: Instagram username
            
        Returns:
            Інформація про користувача або None
        """
        try:
            user = self.client.user_info_by_username(username)
            return {
                "user_id": user.pk,
                "username": user.username,
                "full_name": user.full_name,
                "bio": user.biography,
                "follower_count": user.follower_count,
                "following_count": user.following_count,
                "media_count": user.media_count,
                "is_private": user.is_private,
                "is_business": user.is_business,
            }
        except Exception as e:
            logger.error(f"Error getting user info for {username}: {e}")
            return None
