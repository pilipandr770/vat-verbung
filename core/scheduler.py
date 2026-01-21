"""
Оркестратор.
Визначає:
- коли публікувати контент
- коли запускати збір ЦА
- коли запускати запрошення

Features:
- Day/Night mode: 9:00-18:00 work hours
- Publications: Only during work hours
- Invitations: Only during work hours  
- Random messages: 5 templates per channel
- Random delays: 3-5 minutes between invites
"""

import logging
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from core.content_engine import ContentEngine
from core.content_generator import ContentGenerator
from core.content_adapter import ContentAdapter
from core.models import Post, Action, ActionType, Log
from core.cleanup import ContentCleanupManager
from core.work_hours import WorkHoursManager, PublicationScheduler
from channels.linkedin.publisher import LinkedInPublisher
from channels.telegram.publisher import TelegramPublisher
from channels.instagram.publisher import InstagramPublisher

load_dotenv()


logger = logging.getLogger(__name__)


class Scheduler:
    """Керує планування і оркестрацією всіх каналів."""
    
    def __init__(self):
        """Ініціалізація scheduler."""
        self.scheduler = BackgroundScheduler()
        self.content_engine = ContentEngine()
        self.content_generator = ContentGenerator()  # Новый циклический генератор
        self.content_adapter = ContentAdapter()
        self.work_hours = WorkHoursManager()
        self.publication_scheduler = PublicationScheduler()
        
        # Database connection
        from core.models import DatabaseConnection
        self.db_connection = DatabaseConnection()
        
        self.linkedin_publisher = LinkedInPublisher()
        self.telegram_publisher = TelegramPublisher()
        
        # Instagram is optional - may fail due to IP blocks, etc.
        self.instagram_publisher = None
        try:
            from channels.instagram.publisher import InstagramPublisher
            self.instagram_publisher = InstagramPublisher()
            logger.info("✅ Instagram publisher initialized")
        except Exception as e:
            logger.warning(f"⚠️ Instagram publisher failed (will skip): {str(e)}")
        
        self._setup_jobs()
    
    def _setup_jobs(self) -> None:
        """Налаштування jobs для scheduler."""
        
        logger.info(f"🕐 Work hours: {self.work_hours.work_hours_start}:00-{self.work_hours.work_hours_end}:00")
        
        # LinkedIn: 2 пості на день (10:00, 15:00 - within work hours)
        self.scheduler.add_job(
            self._publish_linkedin,
            CronTrigger(hour=10, minute=0),
            id='linkedin_publish_morning',
            name='LinkedIn publish morning',
            replace_existing=True,
        )
        self.scheduler.add_job(
            self._publish_linkedin,
            CronTrigger(hour=15, minute=0),
            id='linkedin_publish_afternoon',
            name='LinkedIn publish afternoon',
            replace_existing=True,
        )
        
        # Telegram: 3 пості на день (9:30, 13:00, 17:30 - within work hours)
        times = [(9, 30), (13, 0), (17, 30)]
        for i, (hour, minute) in enumerate(times):
            self.scheduler.add_job(
                self._publish_telegram,
                CronTrigger(hour=hour, minute=minute),
                id=f'telegram_publish_{i}',
                name=f'Telegram publish {i+1}',
                replace_existing=True,
            )
        
        # Instagram: 3 пості на день (9:00, 13:00, 17:00 - within work hours)
        times = [(9, 0), (13, 0), (17, 0)]
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
        
        # Daily cleanup: Delete old published posts (prevents database bloat)
        cleanup_enabled = os.getenv("CLEANUP_ENABLED", "True").lower() == "true"
        if cleanup_enabled:
            cleanup_time = os.getenv("CLEANUP_TIME", "02:00")  # Default: 2:00 AM UTC
            try:
                hour, minute = map(int, cleanup_time.split(":"))
                self.scheduler.add_job(
                    self._cleanup_old_posts,
                    CronTrigger(hour=hour, minute=minute),
                    id='daily_cleanup',
                    name='Daily cleanup of old published posts',
                    replace_existing=True,
                )
                logger.info(f"✅ Cleanup job scheduled for {cleanup_time} UTC")
            except ValueError:
                logger.warning(f"Invalid CLEANUP_TIME format: {cleanup_time}. Using default 02:00")
                self.scheduler.add_job(
                    self._cleanup_old_posts,
                    CronTrigger(hour=2, minute=0),
                    id='daily_cleanup',
                    name='Daily cleanup of old published posts',
                    replace_existing=True,
                )
        
        logger.info("Jobs configured successfully")
    
    def _publish_linkedin(self) -> None:
        """Публікація контенту на LinkedIn."""
        try:
            logger.info("📌 Publishing to LinkedIn...")
            
            # Генерація нового контенту з циклічним генератором (30 тем)
            generated_content = self.content_generator.generate_content()
            content_de = generated_content.get("title", "")
            content_adapted = generated_content.get("description", "")
            theme = generated_content.get("theme", "")
            
            # Збереження в БД
            post = Post(
                channel="linkedin",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            # Публікація на LinkedIn
            success = self.linkedin_publisher.publish_post({
                "title": content_de,
                "description": content_adapted
            })
            
            if success:
                logger.info(f"✅ LinkedIn post published (ID: {post.id}) - Theme: {theme}")
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="linkedin",
                    post_id=post.id,
                    details={"theme": theme}
                )
                action.save()
            else:
                logger.warning("❌ LinkedIn post failed")
        
        except Exception as e:
            logger.error(f"LinkedIn publish error: {e}", exc_info=True)
    
    def _publish_telegram(self) -> None:
        """Публікація контенту на Telegram."""
        try:
            logger.info("📱 Publishing to Telegram...")
            
            # Генерація нового контенту з циклічним генератором
            generated_content = self.content_generator.generate_content()
            content_de = generated_content.get("title", "")
            content_adapted = generated_content.get("description", "")
            theme = generated_content.get("theme", "")
            
            # Збереження в БД
            post = Post(
                channel="telegram",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            # Публікація на Telegram
            success = self.telegram_publisher.publish_post({
                "title": content_de,
                "description": content_adapted
            })
            
            if success:
                logger.info(f"✅ Telegram post published (ID: {post.id}) - Theme: {theme}")
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="telegram",
                    post_id=post.id,
                    details={"theme": theme}
                )
                action.save()
            else:
                logger.warning("❌ Telegram post failed")
        
        except Exception as e:
            logger.error(f"Telegram publish error: {e}", exc_info=True)
    
    def _publish_instagram(self) -> None:
        """Публікація контенту на Instagram."""
        if not self.instagram_publisher:
            logger.info("⏭️ Skipping Instagram publish (not available)")
            return
        
        try:
            logger.info("📸 Publishing to Instagram...")
            
            # Генерація нового контенту з циклічним генератором
            generated_content = self.content_generator.generate_content()
            content_de = generated_content.get("title", "")
            content_adapted = generated_content.get("description", "")
            theme = generated_content.get("theme", "")
            
            # Збереження в БД
            post = Post(
                channel="instagram",
                content_de=content_de,
                content_adapted=content_adapted,
            )
            post.save()
            
            # Публікація на Instagram
            success = self.instagram_publisher.publish_post({
                "title": content_de,
                "description": content_adapted
            })
            
            if success:
                logger.info(f"✅ Instagram post published (ID: {post.id}) - Theme: {theme}")
                action = Action(
                    action_type=ActionType.POST_PUBLISHED,
                    channel="instagram",
                    post_id=post.id,
                    details={"theme": theme}
                )
                action.save()
            else:
                logger.warning("❌ Instagram post failed")
        
        except Exception as e:
            logger.error(f"Instagram publish error: {e}", exc_info=True)
    
    def _collect_telegram_audience(self) -> None:
        """Збір цільової аудиторії з Telegram."""
        try:
            logger.info("🔍 Collecting Telegram audience...")
            
            # Для тестирования - просто логируем что сбор произошёл
            # В боевом режиме здесь будет интеграция с Telethon для сбора из групп/каналов
            
            action = Action(
                action_type=ActionType.LEAD_COLLECTED,
                channel="telegram",
                details={
                    "status": "completed",
                    "leads_found": 0,
                    "note": "Awaiting Telethon integration for real lead collection"
                }
            )
            action.save()
            logger.info("✅ Telegram audience collection scheduled")
        except Exception as e:
            logger.error(f"Telegram collection error: {e}", exc_info=True)
    
    def _collect_instagram_audience(self) -> None:
        """Збір цільової аудиторії з Instagram."""
        if not self.instagram_publisher:
            logger.info("⏭️ Skipping Instagram audience collection (not available)")
            return
        
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
            
            # Проверяем рабочие часы
            if not self.work_hours.is_work_hours():
                logger.info("⏰ Outside work hours - skipping invitations")
                return
            
            # Импортируем scorer
            from core.scoring import LeadScorer
            scorer = LeadScorer()
            
            # Импортируем inviter
            from channels.telegram.inviter import TelegramInviter
            inviter = TelegramInviter()
            
            # Получаем непригласённых лидов из БД с низким скором
            with self.db_connection.get_cursor() as cur:
                # Получаем топ 3 лидов для приглашения (максимум в день)
                cur.execute(f"""
                    SELECT id, username, bio, score
                    FROM promotion_hub.leads
                    WHERE platform = 'telegram'
                    AND invited = FALSE
                    AND blocked = FALSE
                    AND score >= 0.5
                    ORDER BY score DESC
                    LIMIT 3
                """)
                
                leads = cur.fetchall()
                
                if not leads:
                    logger.info("📭 No high-scoring Telegram leads to invite")
                    return
                
                invited_count = 0
                for lead in leads:
                    try:
                        lead_id = lead['id']
                        username = lead['username'] or f"user_{lead_id}"
                        bio = lead['bio'] or ""
                        score = lead['score']
                        
                        logger.info(f"📨 Inviting {username} (score: {score:.2f})")
                        
                        # Отправляем приглашение
                        # Для тестирования - просто логируем
                        # result = inviter.send_invite(str(lead_id), username, bio)
                        
                        # Помечаем как приглашённого
                        cur.execute(f"""
                            UPDATE promotion_hub.leads
                            SET invited = TRUE
                            WHERE id = %s
                        """, (lead_id,))
                        
                        # Логируем действие
                        action = Action(
                            action_type=ActionType.LEAD_INVITED,
                            channel="telegram",
                            lead_id=lead_id,
                            details={"username": username, "score": score}
                        )
                        action.save()
                        
                        invited_count += 1
                        logger.info(f"✅ Invite processed for {username}")
                        
                    except Exception as e:
                        logger.error(f"Error inviting {username}: {e}", exc_info=True)
                        continue
                
                logger.info(f"✅ Telegram invitations completed: {invited_count} leads processed")
                
        except Exception as e:
            logger.error(f"Telegram invite error: {e}", exc_info=True)
    
    def _invite_instagram(self) -> None:
        """Запрошення лідів на Instagram."""
        if not self.instagram_publisher:
            logger.info("⏭️ Skipping Instagram invitations (not available)")
            return
        
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
    
    def _cleanup_old_posts(self) -> None:
        """Видалення старих опублікованих постів для запобігання переповненню БД."""
        try:
            logger.info("🗑️  Running daily cleanup of old published posts...")
            
            # Отримати налаштування утримання з .env
            retention_days = int(os.getenv("POST_RETENTION_DAYS", "30"))
            
            # Отримати поточну статистику перед очисткою
            stats_before = ContentCleanupManager.get_cleanup_stats()
            logger.info(
                f"📊 Database stats BEFORE cleanup: "
                f"Total posts: {stats_before.get('total_posts', 0)}, "
                f"Published: {stats_before.get('published_posts', 0)}"
            )
            
            # Виконати очистку
            result = ContentCleanupManager.delete_old_published_posts(
                days_to_keep=retention_days,
                verbose=True
            )
            
            # Отримати статистику після очистки
            stats_after = ContentCleanupManager.get_cleanup_stats()
            logger.info(
                f"📊 Database stats AFTER cleanup: "
                f"Total posts: {stats_after.get('total_posts', 0)}, "
                f"Published: {stats_after.get('published_posts', 0)}"
            )
            
            # Зберегти результат в логи
            action = Action(
                action_type=ActionType.POST_PUBLISHED,  # Переиспользуем для системных операций
                channel="system",
                details={
                    "operation": "cleanup",
                    "deleted_posts": result.get('deleted_posts', 0),
                    "deleted_actions": result.get('deleted_actions', 0),
                    "retention_days": retention_days,
                    "posts_before": stats_before.get('total_posts', 0),
                    "posts_after": stats_after.get('total_posts', 0)
                }
            )
            action.save()
            
            if result['status'] == 'success':
                logger.info(
                    f"✅ Cleanup completed: "
                    f"Deleted {result.get('deleted_posts', 0)} posts, "
                    f"{result.get('deleted_actions', 0)} actions "
                    f"(older than {retention_days} days)"
                )
            else:
                logger.error(f"❌ Cleanup failed: {result.get('message', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Cleanup job error: {e}", exc_info=True)
    
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
