"""
Моделі БД (PostgreSQL).
Leads, Posts, Actions, Logs.

Використовує psycopg2 для прямого управління PostgreSQL.
search_path встановлюється автоматично при підключенні.
"""

import os
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor, Json
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


class ActionType(str, Enum):
    """Типи дій в системі."""
    POST_PUBLISHED = "post_published"
    LEAD_COLLECTED = "lead_collected"
    LEAD_ANALYZED = "lead_analyzed"
    LEAD_INVITED = "lead_invited"
    LEAD_SKIPPED = "lead_skipped"


class DatabaseConnection:
    """Менеджер підключення до PostgreSQL."""
    
    def __init__(self):
        """Ініціалізація з параметрами з .env."""
        self.database_url = os.getenv("DATABASE_URL")
        self.db_schema = os.getenv("DB_SCHEMA", "promotion_hub")
        
        if not self.database_url:
            raise ValueError("DATABASE_URL не встановлена в .env")
    
    @contextmanager
    def get_connection(self):
        """Context manager для отримання підключення."""
        conn = psycopg2.connect(self.database_url)
        try:
            # Встановлення схеми за замовчуванням
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("SET search_path TO {}, public")
                    .format(sql.Identifier(self.db_schema))
                )
            conn.commit()
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def get_cursor(self, commit=True):
        """Context manager для отримання курсора."""
        with self.get_connection() as conn:
            cur = conn.cursor(cursor_factory=DictCursor)
            try:
                yield cur
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Database error: {e}")
                raise
            finally:
                cur.close()


# Глобальний екземпляр підключення
_db = DatabaseConnection()


class Lead:
    """Модель лідів."""
    
    TABLE_NAME = "leads"
    
    def __init__(
        self,
        source: str,
        platform: str,
        identifier: str,
        email: Optional[str] = None,
        username: Optional[str] = None,
        bio: Optional[str] = None,
        score: float = 0.0,
        invited: bool = False,
        blocked: bool = False,
        created_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.source = source
        self.platform = platform
        self.identifier = identifier
        self.email = email
        self.username = username
        self.bio = bio
        self.score = score
        self.invited = invited
        self.blocked = blocked
        self.created_at = created_at or datetime.utcnow()
    
    def save(self) -> int:
        """Зберігає лід в БД. Повертає ID."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    INSERT INTO {table} 
                    (source, platform, identifier, email, username, bio, score, invited, blocked, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                ).format(table=sql.Identifier(self.TABLE_NAME)),
                (
                    self.source, self.platform, self.identifier,
                    self.email, self.username, self.bio,
                    self.score, self.invited, self.blocked,
                    self.created_at
                )
            )
            self.id = cur.fetchone()["id"]
            logger.info(f"Lead saved: {self.identifier} (ID: {self.id})")
            return self.id
    
    def update_score(self, new_score: float) -> None:
        """Оновляє скор лідів."""
        if not self.id:
            raise ValueError("Lead must be saved before updating")
        
        self.score = new_score
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL("UPDATE {table} SET score = %s WHERE id = %s")
                .format(table=sql.Identifier(self.TABLE_NAME)),
                (new_score, self.id)
            )
            logger.debug(f"Lead score updated: {self.id} -> {new_score}")
    
    def mark_invited(self) -> None:
        """Позначає лід як запрошений."""
        if not self.id:
            raise ValueError("Lead must be saved before marking")
        
        self.invited = True
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL("UPDATE {table} SET invited = TRUE WHERE id = %s")
                .format(table=sql.Identifier(self.TABLE_NAME)),
                (self.id,)
            )
            logger.info(f"Lead marked as invited: {self.id}")
    
    def mark_blocked(self) -> None:
        """Позначає лід як заблокований."""
        if not self.id:
            raise ValueError("Lead must be saved before blocking")
        
        self.blocked = True
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL("UPDATE {table} SET blocked = TRUE WHERE id = %s")
                .format(table=sql.Identifier(self.TABLE_NAME)),
                (self.id,)
            )
            logger.info(f"Lead marked as blocked: {self.id}")
    
    @staticmethod
    def get_by_identifier(platform: str, identifier: str) -> Optional["Lead"]:
        """Отримує лід за платформою і identifier."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT * FROM {table} WHERE platform = %s AND identifier = %s"
                ).format(table=sql.Identifier(Lead.TABLE_NAME)),
                (platform, identifier)
            )
            row = cur.fetchone()
            if not row:
                return None
            
            return Lead(
                id=row["id"],
                source=row["source"],
                platform=row["platform"],
                identifier=row["identifier"],
                email=row["email"],
                username=row["username"],
                bio=row["bio"],
                score=row["score"],
                invited=row["invited"],
                blocked=row["blocked"],
                created_at=row["created_at"],
            )


class Post:
    """Модель постів."""
    
    TABLE_NAME = "posts"
    
    def __init__(
        self,
        channel: str,
        content_de: str,
        content_adapted: str,
        language: str = "de",
        published: bool = False,
        published_at: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.channel = channel
        self.content_de = content_de
        self.content_adapted = content_adapted
        self.language = language
        self.published = published
        self.published_at = published_at
        self.created_at = created_at or datetime.utcnow()
    
    def save(self) -> int:
        """Зберігає пост в БД."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    INSERT INTO {table}
                    (channel, content_de, content_adapted, language, published, published_at, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                ).format(table=sql.Identifier(self.TABLE_NAME)),
                (
                    self.channel, self.content_de, self.content_adapted,
                    self.language, self.published, self.published_at,
                    self.created_at
                )
            )
            self.id = cur.fetchone()["id"]
            logger.info(f"Post saved: {self.channel} (ID: {self.id})")
            return self.id
    
    def mark_published(self) -> None:
        """Позначає пост як опублікований."""
        if not self.id:
            raise ValueError("Post must be saved before marking")
        
        self.published = True
        self.published_at = datetime.utcnow()
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    "UPDATE {table} SET published = TRUE, published_at = %s WHERE id = %s"
                ).format(table=sql.Identifier(self.TABLE_NAME)),
                (self.published_at, self.id)
            )
            logger.info(f"Post marked as published: {self.id}")


class Action:
    """Модель дій."""
    
    TABLE_NAME = "actions"
    
    def __init__(
        self,
        action_type: ActionType,
        channel: str,
        lead_id: Optional[int] = None,
        post_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.action_type = action_type
        self.channel = channel
        self.lead_id = lead_id
        self.post_id = post_id
        self.details = details or {}
        self.created_at = created_at or datetime.utcnow()
    
    def save(self) -> int:
        """Зберігає дію в БД."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    INSERT INTO {table}
                    (action_type, channel, lead_id, post_id, details, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                ).format(table=sql.Identifier(self.TABLE_NAME)),
                (
                    self.action_type.value, self.channel,
                    self.lead_id, self.post_id,
                    Json(self.details), self.created_at
                )
            )
            self.id = cur.fetchone()["id"]
            logger.debug(f"Action logged: {self.action_type.value} (ID: {self.id})")
            return self.id


class Log:
    """Модель логів."""
    
    TABLE_NAME = "logs"
    
    def __init__(
        self,
        message: str,
        level: str = "INFO",
        created_at: Optional[datetime] = None,
    ):
        self.message = message
        self.level = level
        self.created_at = created_at or datetime.utcnow()
    
    def save(self) -> None:
        """Зберігає лог в БД."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    INSERT INTO {table}
                    (message, level, created_at)
                    VALUES (%s, %s, %s)
                    """
                ).format(table=sql.Identifier(Log.TABLE_NAME)),
                (self.message, self.level, self.created_at)
            )
    
    @staticmethod
    def get_recent(limit: int = 10) -> List["Log"]:
        """Отримує останні логи."""
        with _db.get_cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT * FROM {table} ORDER BY created_at DESC LIMIT %s"
                ).format(table=sql.Identifier(Log.TABLE_NAME)),
                (limit,)
            )
            rows = cur.fetchall()
            return [
                Log(
                    message=row["message"],
                    level=row["level"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]
