"""
Оркестратор.
Визначає:
- коли публікувати контент
- коли запускати збір ЦА
- коли запускати запрошення
"""

import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from core.content_engine import ContentEngine
from core.content_adapter import ContentAdapter
from core.models import Post, Action, ActionType, Log
from channels.linkedin.publisher import LinkedInPublisher
from channels.telegram.publisher import TelegramPublisher
from channels.instagram.publisher import InstagramPublisher


logger = logging.getLogger(__name__)


class Scheduler:
    """Керує планування і оркестрацією всіх каналів."""
    
    def __init__(self):
        """Ініціалізація scheduler."""
        self.scheduler = BackgroundScheduler()
        self.content_engine = ContentEngine()
        self.content_adapter = ContentAdapter()
        
        self.linkedin_publisher = LinkedInPublisher()
        self.telegram_publisher = TelegramPublisher()
        self.instagram_publisher = InstagramPublisher()
        
        self._setup_jobs()
    
    def _setup_jobs(self) -> None:
        """Налаштування jobs для scheduler."""
        
        # LinkedIn: 2 пости на день (08:00, 14:00 CET)
        self.scheduler.add_job(
            self._publish_linkedin,
            CronTrigger(hour=8, minute=0),
            id='linkedin_publish_morning',
            name='LinkedIn publish morning',
            replace_existing=True,
        )
        self.scheduler.add_job(
            self._publish_linkedin,
            CronTrigger(hour=14, minute=0),
            id='linkedin_publish_afternoon',
            name='LinkedIn publish afternoon',
            replace_existing=True,
        )
        
        # Telegram: 5 постів на день (розподілено)
        times = [(9, 0), (11, 30), (14, 0), (17, 0), (19, 30)]
        for i, (hour, minute) in enumerate(times):
            self.scheduler.add_job(
                self._publish_telegram,
                CronTrigger(hour=hour, minute=minute),
                id=f'telegram_publish_{i}',
                name=f'Telegram publish {i+1}',
                replace_existing=True,
            )
        
        # Instagram: 3 пості на день (09:00, 13:00, 19:00 CET)
        times = [(9, 0), (13, 0), (19, 0)]
        for i, (hour, minute) in enumerate(times):
            self.scheduler.add_job(
                self._publish_instagram,
                CronTrigger(hour=hour, minute=minute),
                id=f'instagram_publish_{i}',
                name=f'Instagram publish {i+1}',
                replace_existing=True,
            )
        
        # Telegram: Збір аудиторії (кожні 6 годин)
        self.scheduler.add_job(
            self._collect_telegram_audience,
            CronTrigger(hour='*/6'),
            id='telegram_collect',
            name='Telegram collect audience',
            replace_existing=True,
        )
        
        # Instagram: Збір аудиторії (кожні 8 годин)
        self.scheduler.add_job(
            self._collect_instagram_audience,
            CronTrigger(hour='*/8'),
            id='instagram_collect',
            name='Instagram collect audience',
            replace_existing=True,
        )
        
        # Telegram: Запрошення (кожні 2 години, макс 10 на день)
        self.scheduler.add_job(
            self._invite_telegram,
            CronTrigger(hour='*/2'),
            id='telegram_invite',
            name='Telegram invite',
            replace_existing=True,
        )
        
        # Instagram: Запрошення (кожні 3 години, макс 8 на день)
        self.scheduler.add_job(
            self._invite_instagram,
            CronTrigger(hour='*/3'),
            id='instagram_invite',
            name='Instagram invite',
            replace_existing=True,
        )
        
        logger.info("Jobs configured successfully")
    
    def _publish_linkedin(self) -> None:
        """Публікація контенту на LinkedIn."""
        try:
            logger.info("📌 Publishing to LinkedIn...")
            
            # Генерація контенту
            topic = self.content_engine.get_random_topic()
            content_de = self.content_engine.generate_content(topic)
            content_adapted = self.content_adapter.adapt(content_de, "linkedin")
            
            # Збереження в БД
            post = Post(
                channel="linkedin",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            # Публікація
            success = self.linkedin_publisher.publish_post(content_adapted)
            
            if success:
                post.mark_published()
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="linkedin",
                    post_id=post.id,
                    details={"topic": topic.value}
                )
                action.save()
                logger.info(f"✅ LinkedIn post published (ID: {post.id})")
            else:
                logger.warning("❌ LinkedIn post failed")
        
        except Exception as e:
            logger.error(f"LinkedIn publish error: {e}", exc_info=True)
    
    def _publish_telegram(self) -> None:
        """Публікація контенту на Telegram."""
        try:
            logger.info("📱 Publishing to Telegram...")
            
            topic = self.content_engine.get_random_topic()
            content_de = self.content_engine.generate_content(topic)
            content_adapted = self.content_adapter.adapt(content_de, "telegram")
            
            post = Post(
                channel="telegram",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            success = self.telegram_publisher.publish_post(content_adapted)
            
            if success:
                post.mark_published()
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="telegram",
                    post_id=post.id,
                    details={"topic": topic.value}
                )
                action.save()
                logger.info(f"✅ Telegram post published (ID: {post.id})")
            else:
                logger.warning("❌ Telegram post failed")
        
        except Exception as e:
            logger.error(f"Telegram publish error: {e}", exc_info=True)
    
    def _publish_instagram(self) -> None:
        """Публікація контенту на Instagram."""
        try:
            logger.info("📸 Publishing to Instagram...")
            
            topic = self.content_engine.get_random_topic()
            content_de = self.content_engine.generate_content(topic)
            content_adapted = self.content_adapter.adapt(content_de, "instagram")
            
            post = Post(
                channel="instagram",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            success = self.instagram_publisher.publish_post(content_adapted)
            
            if success:
                post.mark_published()
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="instagram",
                    post_id=post.id,
                    details={"topic": topic.value}
                )
                action.save()
                logger.info(f"✅ Instagram post published (ID: {post.id})")
            else:
                logger.warning("❌ Instagram post failed")
        
        except Exception as e:
            logger.error(f"Instagram publish error: {e}", exc_info=True)
    
    def _collect_telegram_audience(self) -> None:
        """Збір цільової аудиторії з Telegram."""
        try:
            logger.info("🔍 Collecting Telegram audience...")
            # TODO: Реалізація після інтеграції Telegram API
            action = Action(
                action_type=ActionType.LEAD_COLLECTED,
                channel="telegram",
                details={"status": "scheduled"}
            )
            action.save()
        except Exception as e:
            logger.error(f"Telegram collection error: {e}", exc_info=True)
    
    def _collect_instagram_audience(self) -> None:
        """Збір цільової аудиторії з Instagram."""
        try:
            logger.info("🔍 Collecting Instagram audience...")
            # TODO: Реалізація після інтеграції Instagram API
            action = Action(
                action_type=ActionType.LEAD_COLLECTED,
                channel="instagram",
                details={"status": "scheduled"}
            )
            action.save()
        except Exception as e:
            logger.error(f"Instagram collection error: {e}", exc_info=True)
    
    def _invite_telegram(self) -> None:
        """Запрошення лідів на Telegram."""
        try:
            logger.info("💬 Processing Telegram invitations...")
            # TODO: Реалізація після scoring та rules
            action = Action(
                action_type=ActionType.LEAD_INVITED,
                channel="telegram",
                details={"status": "scheduled"}
            )
            action.save()
        except Exception as e:
            logger.error(f"Telegram invite error: {e}", exc_info=True)
    
    def _invite_instagram(self) -> None:
        """Запрошення лідів на Instagram."""
        try:
            logger.info("💬 Processing Instagram invitations...")
            # TODO: Реалізація після scoring та rules
            action = Action(
                action_type=ActionType.LEAD_INVITED,
                channel="instagram",
                details={"status": "scheduled"}
            )
            action.save()
        except Exception as e:
            logger.error(f"Instagram invite error: {e}", exc_info=True)
    
    def run(self) -> None:
        """Запуск scheduler."""
        try:
            logger.info("🚀 Promotion Hub Scheduler started")
            self.scheduler.start()
            
            # Блокуючий цикл
            import time
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Scheduler shutdown initiated...")
            self.stop()
    
    def stop(self) -> None:
        """Зупинення scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
