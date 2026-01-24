"""
Client Configuration Manager
Централизованное управление настройками клиента для масштабируемости
"""

import json
import os
import logging
from typing import Dict, List, Set, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ClientConfig:
    """Управление конфигурацией клиента для унифицированного доступа."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Инициализация конфигурации клиента.

        Args:
            config_path: Путь к файлу конфигурации (опционально)
        """
        if config_path is None:
            # По умолчанию ищем в папке client_config
            current_dir = Path(__file__).parent.parent
            config_path = current_dir / "client_config" / "client_config.json"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Загрузка конфигурации из файла."""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found: {self.config_path}")
                self._create_default_config()
                return

            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)

            logger.info(f"Client config loaded from: {self.config_path}")
            logger.info(f"Client: {self.get_client_name()}")

        except Exception as e:
            logger.error(f"Error loading client config: {e}")
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Создание дефолтной конфигурации при отсутствии файла."""
        logger.warning("Using default configuration")
        self._config = {
            "client_info": {"name": "Default Client"},
            "b2b_keywords": {
                "common": ["business", "company"],
                "industry_specific": [],
                "job_titles": ["manager", "director"],
                "german_business_terms": []
            },
            "scoring_rules": {
                "thresholds": {"invite": 0.6, "save": 0.3, "block": 0.1}
            }
        }

    def reload_config(self) -> None:
        """Перезагрузка конфигурации."""
        self._load_config()

    # === CLIENT INFO ===

    def get_client_name(self) -> str:
        """Получить имя клиента."""
        return self._config.get("client_info", {}).get("name", "Unknown Client")

    def get_client_info(self) -> Dict[str, Any]:
        """Получить информацию о клиенте."""
        return self._config.get("client_info", {})

    # === B2B KEYWORDS ===

    def get_b2b_keywords(self) -> Set[str]:
        """Получить все B2B ключевые слова."""
        keywords = set()

        # Собираем из всех категорий
        for category in ["common", "industry_specific", "job_titles", "german_business_terms"]:
            category_keywords = self._config.get("b2b_keywords", {}).get(category, [])
            keywords.update(category_keywords)

        return keywords

    def get_b2b_keywords_by_category(self, category: str) -> List[str]:
        """Получить ключевые слова по категории."""
        return self._config.get("b2b_keywords", {}).get(category, [])

    # === SCORING RULES ===

    def get_scoring_thresholds(self) -> Dict[str, float]:
        """Получить пороги скоринга."""
        return self._config.get("scoring_rules", {}).get("thresholds", {
            "invite": 0.6,
            "save": 0.3,
            "block": 0.1
        })

    def get_scoring_weights(self) -> Dict[str, float]:
        """Получить веса для скоринга."""
        return self._config.get("scoring_rules", {}).get("weights", {})

    def get_platform_multiplier(self, platform: str) -> float:
        """Получить множитель для платформы."""
        multipliers = self._config.get("scoring_rules", {}).get("platform_multipliers", {})
        return multipliers.get(platform, 1.0)

    # === CONTENT TOPICS ===

    def get_content_topics(self) -> List[str]:
        """Получить темы контента."""
        return self._config.get("content_topics", [])

    # === PLATFORM SETTINGS ===

    def get_target_platforms(self) -> Dict[str, Dict[str, Any]]:
        """Получить настройки платформ."""
        return self._config.get("target_platforms", {})

    def is_platform_enabled(self, platform: str) -> bool:
        """Проверить, включена ли платформа."""
        platform_config = self._config.get("target_platforms", {}).get(platform, {})
        return platform_config.get("enabled", False)

    def get_platform_setting(self, platform: str, setting: str) -> Any:
        """Получить настройку платформы."""
        platform_config = self._config.get("target_platforms", {}).get(platform, {})
        return platform_config.get(setting)

    # === COLLECTION LIMITS ===

    def get_collection_limits(self) -> Dict[str, int]:
        """Получить лимиты сбора."""
        return self._config.get("collection_limits", {
            "max_leads_per_job": 50,
            "max_followers_per_account": 100,
            "max_invites_per_lead": 1
        })

    # === SAFETY LIMITS ===

    def get_safety_limits(self) -> Dict[str, int]:
        """Получить лимиты безопасности."""
        return self._config.get("safety_limits", {
            "work_hours_start": 9,
            "work_hours_end": 18,
            "invitation_delay_min": 180,
            "invitation_delay_max": 300
        })

    # === AI SETTINGS ===

    def get_ai_settings(self) -> Dict[str, Any]:
        """Получить настройки AI."""
        return self._config.get("ai_content_settings", {
            "language": "DE",
            "provider": "openai",
            "model": "gpt-3.5-turbo"
        })

    # === CONTENT TOPICS ===

    def get_content_topics(self) -> List[str]:
        """Получить доступные темы контента."""
        return self._config.get("content_topics", [
            "compliance", "bi", "verification", "integration",
            "security", "efficiency", "trust", "data_quality"
        ])

    # === MONITORING ===

    def get_monitoring_settings(self) -> Dict[str, Any]:
        """Получить настройки мониторинга."""
        return self._config.get("monitoring", {
            "enable_logging": True,
            "log_level": "INFO"
        })

    # === UTILITY METHODS ===

    def get_config_value(self, path: str, default: Any = None) -> Any:
        """
        Получить значение по пути (dot notation).

        Args:
            path: Путь типа "scoring_rules.thresholds.invite"
            default: Значение по умолчанию
        """
        keys = path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def validate_config(self) -> List[str]:
        """Валидация конфигурации."""
        errors = []

        # Проверяем обязательные поля
        required_fields = [
            "client_info.name",
            "b2b_keywords",
            "scoring_rules.thresholds"
        ]

        for field in required_fields:
            if self.get_config_value(field) is None:
                errors.append(f"Missing required field: {field}")

        # Проверяем пороги скоринга
        thresholds = self.get_scoring_thresholds()
        if thresholds.get("invite", 0) <= thresholds.get("save", 0):
            errors.append("Invite threshold must be higher than save threshold")

        return errors

    def __str__(self) -> str:
        """Строковое представление."""
        return f"ClientConfig(client='{self.get_client_name()}', platforms={list(self.get_target_platforms().keys())})"


# Глобальный экземпляр для удобного доступа
_client_config: Optional[ClientConfig] = None


def get_client_config() -> ClientConfig:
    """Получить глобальный экземпляр конфигурации."""
    global _client_config
    if _client_config is None:
        _client_config = ClientConfig()
    return _client_config


def reload_client_config() -> None:
    """Перезагрузить глобальную конфигурацию."""
    global _client_config
    if _client_config:
        _client_config.reload_config()