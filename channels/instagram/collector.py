"""
Збір ЦА:
підписники схожих акаунтів,
активні користувачі,
коментарі.
"""

import os
import logging
import time
from typing import List, Dict, Optional
from instagrapi import Client
from core.client_config import get_client_config

logger = logging.getLogger(__name__)


class InstagramCollector:
    """Збирає цільову аудиторію з Instagram."""

    def __init__(self):
        """Ініціалізація Instagram collector."""
        self.platform = "instagram"
        self.client = Client()

        # Загружаем конфигурацию клиента
        config = get_client_config()
        self.collection_limits = config.get_collection_limits()
        self.safety_limits = config.get_safety_limits()

        # Завантаження облікових даних
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")

        if not self.username or not self.password:
            raise ValueError("INSTAGRAM_USERNAME та INSTAGRAM_PASSWORD мають бути встановлені")

        self._authenticate()

        logger.info(f"InstagramCollector initialized for client: {config.get_client_name()}")

    def collect_from_similar_accounts(self, account_usernames: List[str], max_followers: Optional[int] = None) -> List[Dict]:
        """
        Збирає лідів з підписників схожих акаунтів.

        Args:
            account_usernames: Список username схожих акаунтів (B2B-орієнтовані)
            max_followers: Максимальна кількість підписників для аналізу на акаунт (опционально)

        Returns:
            Список виявлених лідів
        """
        # Используем значение из конфигурации, если не указано явно
        if max_followers is None:
            max_followers = self.collection_limits.get("max_followers_per_account", 100)

        leads = []
        
        for account_username in account_usernames:
            try:
                logger.info(f"Collecting from account: {account_username}")
                
                # Отримання інформації про акаунт
                user = self.client.user_info_by_username(account_username)
                user_id = user.pk
                
                # Отримання підписників (обмеження: Instagram API дозволяє обмежену кількість)
                followers = self.client.user_followers(user_id, amount=max_followers)
                
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
                        "is_business": follower.is_business,
                        "media_count": follower.media_count or 0,
                    }
                    leads.append(lead)
                    logger.debug(f"Collected lead: {follower.username}")
                
                logger.info(f"✅ Collected {len(followers)} followers from {account_username}")
                
                # Затримка між акаунтами для уникнення обмежень
                time.sleep(3)
            
            except Exception as e:
                logger.error(f"Error collecting from {account_username}: {e}")
                continue
        
        return leads
    
    def collect_from_found_accounts(self, found_accounts: List[Dict], max_followers: int = 30) -> List[Dict]:
        """
        Збирає лідів з підписників знайдених акаунтів (результати пошуку).
        
        Args:
            found_accounts: Список акаунтів з результатів search_accounts
            max_followers: Максимальна кількість підписників для аналізу на акаунт
            
        Returns:
            Список виявлених лідів
        """
        leads = []
        
        for account in found_accounts:
            try:
                username = account['username']
                user_id = account['user_id']
                
                logger.info(f"Deep analyzing followers of: @{username} ({account['follower_count']} followers)")
                
                # Аналізуємо тільки акаунти з достатньою кількістю підписників
                if account['follower_count'] < 500:
                    logger.info(f"Skipping @{username} - too few followers ({account['follower_count']})")
                    continue
                
                # Отримання підписників
                followers = self.client.user_followers(user_id, amount=max_followers)
                
                for follower in followers:
                    # Детальніший аналіз підписника
                    lead = {
                        "platform": "instagram",
                        "identifier": follower.username,
                        "username": follower.username,
                        "user_id": follower.pk,
                        "bio": follower.biography or "",
                        "source": f"followers_of_found_{username}",
                        "source_account": account,  # Зберігаємо інформацію про джерельний акаунт
                        "follower_count": follower.follower_count or 0,
                        "following_count": follower.following_count or 0,
                        "is_private": follower.is_private,
                        "is_business": follower.is_business,
                        "media_count": follower.media_count or 0,
                        "full_name": follower.full_name or "",
                    }
                    leads.append(lead)
                    logger.debug(f"Collected lead from @{username}: {follower.username}")
                
                logger.info(f"✅ Collected {len(followers)} followers from found account @{username}")
                
                # Більша затримка для знайдених акаунтів
                time.sleep(5)
            
            except Exception as e:
                logger.error(f"Error collecting from found account {account.get('username', 'unknown')}: {e}")
                continue
        
        return leads
    
    def search_accounts(self, keywords: List[str], limit: int = 20) -> List[Dict]:
        """
        Шукає Instagram акаунти за ключовими словами.
        
        Args:
            keywords: Ключові слова для пошуку (наприклад: ['Bau', 'Renovierung', 'Immobilien'])
            limit: Максимальна кількість результатів на ключове слово
            
        Returns:
            Список знайдених акаунтів
        """
        accounts = []
        
        for keyword in keywords:
            try:
                logger.info(f"Searching Instagram accounts for: {keyword}")
                
                # Пошук користувачів через Instagram API
                search_results = self.client.search_users(keyword, limit)
                
                for user in search_results:
                    # Фільтруємо тільки бізнес-акаунти або з великою кількістю підписників
                    if (user.is_business or 
                        user.follower_count > 1000 or 
                        keyword.lower() in (user.biography or "").lower() or
                        keyword.lower() in (user.full_name or "").lower()):
                        
                        account_info = {
                            'user_id': user.pk,
                            'username': user.username,
                            'full_name': user.full_name,
                            'bio': user.biography or "",
                            'follower_count': user.follower_count,
                            'following_count': user.following_count,
                            'media_count': user.media_count,
                            'is_private': user.is_private,
                            'is_business': user.is_business,
                            'is_verified': user.is_verified,
                            'search_keyword': keyword,
                            'profile_pic_url': user.profile_pic_url,
                        }
                        accounts.append(account_info)
                        logger.info(f"Found account: @{user.username} ({user.follower_count} followers)")
                
                logger.info(f"✅ Found {len(search_results)} accounts for '{keyword}'")
                
                # Затримка між пошуками для уникнення обмежень
                import time
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error searching for '{keyword}': {e}")
                continue
        
        # Видаляємо дублікати
        unique_accounts = []
        seen_ids = set()
        for account in accounts:
            if account['user_id'] not in seen_ids:
                unique_accounts.append(account)
                seen_ids.add(account['user_id'])
        
        logger.info(f"✅ Total unique accounts found: {len(unique_accounts)}")
        return unique_accounts[:limit * len(keywords)]  # Повертаємо більше результатів
    
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
