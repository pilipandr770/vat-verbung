"""
Моделі БД (PostgreSQL).
Leads, Posts, Actions, Logs.
"""

from datetime import datetime
from enum import Enum
from typing import Optional


class ActionType(str, Enum):
    """Типи дій в системі."""
    POST_PUBLISHED = "post_published"
    LEAD_COLLECTED = "lead_collected"
    LEAD_ANALYZED = "lead_analyzed"
    LEAD_INVITED = "lead_invited"
    LEAD_SKIPPED = "lead_skipped"


class Lead:
    """Модель лідів."""
    
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
        created_at: Optional[datetime] = None,
    ):
        self.source = source
        self.platform = platform
        self.identifier = identifier
        self.email = email
        self.username = username
        self.bio = bio
        self.score = score
        self.invited = invited
        self.created_at = created_at or datetime.utcnow()


class Post:
    """Модель постів."""
    
    def __init__(
        self,
        channel: str,
        content_de: str,
        content_adapted: str,
        language: str = "de",
        published: bool = False,
        published_at: Optional[datetime] = None,
    ):
        self.channel = channel
        self.content_de = content_de
        self.content_adapted = content_adapted
        self.language = language
        self.published = published
        self.published_at = published_at


class Action:
    """Модель дій."""
    
    def __init__(
        self,
        action_type: ActionType,
        channel: str,
        lead_id: Optional[str] = None,
        post_id: Optional[str] = None,
        details: Optional[dict] = None,
        created_at: Optional[datetime] = None,
    ):
        self.action_type = action_type
        self.channel = channel
        self.lead_id = lead_id
        self.post_id = post_id
        self.details = details or {}
        self.created_at = created_at or datetime.utcnow()
