"""
Cleanup manager для видалення публікованого контенту з БД.
Запобігає переповненню бази даних старими постами після публікації.

Використовується:
1. Вручну: cleanup.delete_old_published_posts()
2. Автоматично: scheduler додає daily cleanup job
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from core.models import _db, sql

logger = logging.getLogger(__name__)


class ContentCleanupManager:
    """Менеджер видалення старого контенту з БД."""
    
    POST_TABLE = "posts"
    ACTION_TABLE = "actions"
    
    @staticmethod
    def delete_old_published_posts(
        days_to_keep: int = 30,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Видаляє всі опубліковані пости старіші за N днів.
        
        Args:
            days_to_keep: Кількість днів для зберігання постів (за замовчуванням 30)
            verbose: Логувати детальну інформацію
        
        Returns:
            {'deleted_posts': int, 'deleted_actions': int, 'status': 'success|error', 'message': str}
        
        Приклади:
            # Видалити пости старіші за 30 днів
            result = ContentCleanupManager.delete_old_published_posts(30)
            print(result)  # {'deleted_posts': 45, 'deleted_actions': 45, 'status': 'success', ...}
            
            # Видалити пості старіші за 7 днів
            result = ContentCleanupManager.delete_old_published_posts(7)
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            with _db.get_cursor() as cur:
                # Спочатку знайти ID постів, які будемо видаляти
                cur.execute(
                    sql.SQL(
                        """
                        SELECT id FROM {table}
                        WHERE published = TRUE AND published_at < %s
                        """
                    ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE)),
                    (cutoff_date,)
                )
                post_ids = [row['id'] for row in cur.fetchall()]
                
                deleted_posts = 0
                deleted_actions = 0
                
                if post_ids:
                    # Видалити associated actions
                    cur.execute(
                        sql.SQL(
                            """
                            DELETE FROM {table}
                            WHERE post_id = ANY(%s)
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.ACTION_TABLE)),
                        (post_ids,)
                    )
                    deleted_actions = cur.rowcount
                    
                    # Видалити самі пости
                    cur.execute(
                        sql.SQL(
                            """
                            DELETE FROM {table}
                            WHERE id = ANY(%s)
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE)),
                        (post_ids,)
                    )
                    deleted_posts = cur.rowcount
                
                result = {
                    'status': 'success',
                    'deleted_posts': deleted_posts,
                    'deleted_actions': deleted_actions,
                    'cutoff_date': cutoff_date.isoformat(),
                    'days_to_keep': days_to_keep,
                    'message': f"Видалено {deleted_posts} постів та {deleted_actions} дій"
                }
                
                if verbose:
                    logger.info(
                        f"🗑️  Cleanup completed: "
                        f"{deleted_posts} posts, {deleted_actions} actions deleted "
                        f"(older than {days_to_keep} days)"
                    )
                
                return result
        
        except Exception as e:
            error_msg = f"Cleanup error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'status': 'error',
                'deleted_posts': 0,
                'deleted_actions': 0,
                'message': error_msg
            }
    
    @staticmethod
    def get_cleanup_stats() -> Dict[str, Any]:
        """
        Отримати статистику контенту в БД.
        
        Returns:
            {
                'total_posts': int,
                'published_posts': int,
                'unpublished_posts': int,
                'oldest_post': str (date),
                'newest_post': str (date),
                'average_posts_per_channel': dict
            }
        """
        try:
            with _db.get_cursor() as cur:
                # Загальна статистика
                cur.execute(
                    sql.SQL(
                        """
                        SELECT 
                            COUNT(*) as total,
                            SUM(CASE WHEN published = TRUE THEN 1 ELSE 0 END) as published,
                            SUM(CASE WHEN published = FALSE THEN 1 ELSE 0 END) as unpublished,
                            MIN(created_at) as oldest,
                            MAX(created_at) as newest
                        FROM {table}
                        """
                    ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE))
                )
                stats = cur.fetchone()
                
                # По каналам
                cur.execute(
                    sql.SQL(
                        """
                        SELECT channel, COUNT(*) as count
                        FROM {table}
                        GROUP BY channel
                        ORDER BY count DESC
                        """
                    ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE))
                )
                per_channel = {row['channel']: row['count'] for row in cur.fetchall()}
                
                return {
                    'total_posts': stats['total'] or 0,
                    'published_posts': stats['published'] or 0,
                    'unpublished_posts': stats['unpublished'] or 0,
                    'oldest_post': (stats['oldest'].isoformat() if stats['oldest'] else None),
                    'newest_post': (stats['newest'].isoformat() if stats['newest'] else None),
                    'posts_per_channel': per_channel
                }
        
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {
                'error': str(e),
                'total_posts': 0,
                'published_posts': 0
            }
    
    @staticmethod
    def cleanup_by_channel(
        channel: str,
        days_to_keep: int = 30,
        published_only: bool = True
    ) -> Dict[str, Any]:
        """
        Видалити контент конкретного каналу старіший за N днів.
        
        Args:
            channel: 'linkedin', 'telegram', 'instagram'
            days_to_keep: Кількість днів для зберігання
            published_only: Видаляти тільки опубліковані
        
        Returns:
            {'deleted': int, 'status': 'success|error', 'message': str}
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            with _db.get_cursor() as cur:
                # Знайти пости для видалення
                if published_only:
                    cur.execute(
                        sql.SQL(
                            """
                            SELECT id FROM {table}
                            WHERE channel = %s AND published = TRUE AND published_at < %s
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE)),
                        (channel, cutoff_date)
                    )
                else:
                    cur.execute(
                        sql.SQL(
                            """
                            SELECT id FROM {table}
                            WHERE channel = %s AND created_at < %s
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE)),
                        (channel, cutoff_date)
                    )
                
                post_ids = [row['id'] for row in cur.fetchall()]
                
                if post_ids:
                    # Видалити actions
                    cur.execute(
                        sql.SQL(
                            """
                            DELETE FROM {table}
                            WHERE post_id = ANY(%s)
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.ACTION_TABLE)),
                        (post_ids,)
                    )
                    
                    # Видалити пости
                    cur.execute(
                        sql.SQL(
                            """
                            DELETE FROM {table}
                            WHERE id = ANY(%s)
                            """
                        ).format(table=sql.Identifier(ContentCleanupManager.POST_TABLE)),
                        (post_ids,)
                    )
                    deleted = cur.rowcount
                else:
                    deleted = 0
                
                return {
                    'status': 'success',
                    'channel': channel,
                    'deleted': deleted,
                    'message': f"Видалено {deleted} постів з каналу {channel}"
                }
        
        except Exception as e:
            logger.error(f"Channel cleanup error: {e}")
            return {
                'status': 'error',
                'deleted': 0,
                'message': str(e)
            }


# Простий API для прямого використання
def cleanup_published_posts(days: int = 30, verbose: bool = True) -> Dict[str, Any]:
    """Видалити опубліковані пости старіші за N днів."""
    return ContentCleanupManager.delete_old_published_posts(days, verbose)


def get_database_stats() -> Dict[str, Any]:
    """Отримати статистику БД."""
    return ContentCleanupManager.get_cleanup_stats()


def cleanup_channel(channel: str, days: int = 30) -> Dict[str, Any]:
    """Видалити контент каналу старіший за N днів."""
    return ContentCleanupManager.cleanup_by_channel(channel, days, published_only=True)
