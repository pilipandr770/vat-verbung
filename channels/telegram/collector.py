"""
Збір цільової аудиторії:
читання чатів, каналів, коментарів.
"""

import os
import logging
from typing import List, Dict, Optional
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon import functions
import asyncio

logger = logging.getLogger(__name__)


class TelegramCollector:
    """Збирає цільову аудиторію з Telegram."""
    
    def __init__(self):
        """Ініціалізація Telegram collector."""
        self.platform = "telegram"
        
        # Завантаження облікових даних
        self.api_id = os.getenv("TELEGRAM_API_ID")
        self.api_hash = os.getenv("TELEGRAM_API_HASH")
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not self.api_id or not self.api_hash:
            logger.warning("TELEGRAM_API_ID та TELEGRAM_API_HASH не встановлені. Деякі функції будуть недоступні.")
            self.client = None
        else:
            # Ініціалізація Telethon клієнта
            self.client = TelegramClient('session_name', int(self.api_id), self.api_hash)
            logger.info("Telegram collector initialized with API credentials")
    
    async def search_groups(self, keywords: List[str], limit: int = 50) -> List[Dict]:
        """
        Шукає Telegram групи за ключовими словами.
        
        Args:
            keywords: Ключові слова для пошуку (наприклад: ['Bau', 'Renovierung', 'Immobilien'])
            limit: Максимальна кількість результатів
            
        Returns:
            Список знайдених груп
        """
        if not self.client:
            logger.warning("Telethon client not initialized - API credentials missing")
            return []
        
        groups = []
        
        try:
            await self.client.start()
            
            for keyword in keywords:
                logger.info(f"Searching for groups with keyword: {keyword}")
                
                # Пошук груп через Telegram
                result = await self.client(functions.contacts.SearchRequest(
                    q=keyword,
                    limit=limit
                ))
                
                for chat in result.chats:
                    if hasattr(chat, 'megagroup') and chat.megagroup:  # Групи
                        group_info = {
                            'id': chat.id,
                            'title': chat.title,
                            'username': getattr(chat, 'username', None),
                            'participants_count': getattr(chat, 'participants_count', 0),
                            'keyword': keyword
                        }
                        groups.append(group_info)
                        logger.info(f"Found group: {chat.title} ({chat.id})")
            
            # Видаляємо дублікати
            unique_groups = []
            seen_ids = set()
            for group in groups:
                if group['id'] not in seen_ids:
                    unique_groups.append(group)
                    seen_ids.add(group['id'])
            
            logger.info(f"Found {len(unique_groups)} unique groups")
            return unique_groups[:limit]
            
        except Exception as e:
            logger.error(f"Error searching groups: {e}")
            return []
        finally:
            if self.client:
                await self.client.disconnect()
    
    async def _collect_from_chats_async(self, chat_ids: List[str]) -> List[Dict]:
        """Асинхронна версія collect_from_chats."""
        leads = []
        
        try:
            await self.client.start()
            
            for chat_id in chat_ids:
                try:
                    logger.info(f"Collecting from chat: {chat_id}")
                    
                    # Отримання повідомлень з чату
                    messages = await self.client.get_messages(chat_id, limit=100)
                    
                    for message in messages:
                        if message.sender and message.text:
                            lead = self.parse_message_for_leads(message.text)
                            if lead:
                                lead.update({
                                    'platform': 'telegram',
                                    'identifier': str(message.sender_id),
                                    'source': f'chat_{chat_id}',
                                    'username': getattr(message.sender, 'username', None),
                                    'bio': message.text[:200]
                                })
                                leads.append(lead)
                                logger.info(f"Found lead in chat {chat_id}: {message.sender_id}")
                
                except Exception as e:
                    logger.error(f"Error collecting from chat {chat_id}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in chat collection: {e}")
        finally:
            if self.client:
                await self.client.disconnect()
        
        return leads
    
    def collect_from_chats(self, chat_ids: List[str]) -> List[Dict]:
        """
        Збирає лідів з чатів.
        
        Args:
            chat_ids: ID чатів для сканування
            
        Returns:
            Список виявлених лідів
        """
        # Запуск асинхронної функції
        if self.client:
            return asyncio.run(self._collect_from_chats_async(chat_ids))
        else:
            logger.warning("Telethon client not available - using bot-only mode")
            return []
    
    def collect_from_channels(self, channel_usernames: List[str]) -> List[Dict]:
        """
        Збирає лідів з каналів.
        
        Args:
            channel_usernames: Username публічних каналів
            
        Returns:
            Список виявлених лідів
        """
        # Запуск асинхронної функції
        if self.client:
            return asyncio.run(self._collect_from_channels_async(channel_usernames))
        else:
            logger.warning("Telethon client not available - using bot-only mode")
            return []
    
    async def _collect_from_channels_async(self, channel_usernames: List[str]) -> List[Dict]:
        """Асинхронна версія collect_from_channels."""
        leads = []
        
        try:
            await self.client.start()
            
            for channel_username in channel_usernames:
                try:
                    logger.info(f"Collecting from channel: {channel_username}")
                    
                    # Отримання каналу за username
                    channel = await self.client.get_entity(channel_username)
                    
                    # Отримання останніх повідомлень
                    messages = await self.client.get_messages(channel, limit=50)
                    
                    for message in messages:
                        if message.text:
                            lead = self.parse_message_for_leads(message.text)
                            if lead:
                                lead.update({
                                    'platform': 'telegram',
                                    'identifier': f"channel_{channel.id}_{message.id}",
                                    'source': f'channel_{channel_username}',
                                    'username': channel_username,
                                    'bio': message.text[:200]
                                })
                                leads.append(lead)
                                logger.info(f"Found lead in channel {channel_username}")
                
                except Exception as e:
                    logger.error(f"Error collecting from channel {channel_username}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in channel collection: {e}")
        finally:
            if self.client:
                await self.client.disconnect()
        
        return leads
    
    def parse_message_for_leads(self, message_text: str) -> Optional[Dict]:
        """
        Аналізує повідомлення на предмет інформації про користувача.
        
        Args:
            message_text: Текст повідомлення
            
        Returns:
            Інформація про потенційного ліду або None
        """
        # Пошук контактної інформації (email, посилання)
        import re
        
        # Email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email = re.search(email_pattern, message_text)
        
        # URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message_text)
        
        if email or urls:
            return {
                "email": email.group() if email else None,
                "urls": urls,
                "message_text": message_text[:200],
            }
        
        return None
