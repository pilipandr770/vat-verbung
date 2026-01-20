"""
Публікація постів на нашій LinkedIn-сторінці.
НІЯКОГО outreach і DM.
Тільки публічні пості.
"""

import os
import time
import logging
from typing import Optional
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


class LinkedInPublisher:
    """Публікатор для LinkedIn."""
    
    def __init__(self):
        """Ініціалізація LinkedIn publisher."""
        self.platform = "linkedin"
        self.username = os.getenv("LINKEDIN_USERNAME")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        
        if not self.username or not self.password:
            logger.warning(
                "LINKEDIN_USERNAME та LINKEDIN_PASSWORD не встановлені. "
                "Публікація на LinkedIn недоступна без аутентифікації."
            )
            self.authenticated = False
        else:
            self.authenticated = True
        
        self.browser = None
        self.page = None
    
    def _authenticate(self) -> bool:
        """
        Аутентифікація на LinkedIn через Playwright.
        
        Returns:
            True якщо успішно, False якщо помилка
        """
        try:
            logger.info("Authenticating to LinkedIn...")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Перейти на LinkedIn login
                page.goto("https://www.linkedin.com/login")
                
                # Заповнити форму входу
                page.fill("input#username", self.username)
                page.fill("input#password", self.password)
                page.click("button[type='submit']")
                
                # Очікування завантаження (до 10 секунд)
                page.wait_for_load_state("networkidle", timeout=10000)
                
                # Перевірка, чи успішний вхід
                if "feed" in page.url or "linkedin.com/feed" in page.url:
                    logger.info("✅ LinkedIn authentication successful")
                    self.browser = browser
                    self.page = page
                    return True
                else:
                    logger.error("❌ LinkedIn authentication failed")
                    browser.close()
                    return False
        
        except Exception as e:
            logger.error(f"❌ LinkedIn authentication error: {e}")
            return False
    
    def publish_post(self, content: str, image_url: Optional[str] = None) -> bool:
        """
        Публікує пост на LinkedIn сторінці.
        
        НІЯКИХ DM, тільки пості на сторінці!
        
        Args:
            content: Адаптований контент
            image_url: URL зображення (опціонально)
            
        Returns:
            True якщо успішно, False якщо помилка
        """
        if not self.authenticated:
            logger.warning(
                "LinkedIn publisher not authenticated. Set LINKEDIN_USERNAME "
                "and LINKEDIN_PASSWORD in .env"
            )
            return False
        
        try:
            # Аутентифікація
            if not self.page:
                if not self._authenticate():
                    return False
            
            logger.info("Publishing post to LinkedIn...")
            
            # Перейти на feed
            self.page.goto("https://www.linkedin.com/feed/")
            time.sleep(2)
            
            # Натиснути на кнопку "Start a post"
            start_post_button = self.page.query_selector(
                "button:has-text('Start a post')"
            )
            
            if not start_post_button:
                logger.error("Could not find 'Start a post' button")
                return False
            
            start_post_button.click()
            time.sleep(1)
            
            # Заповнити текст посту
            textarea = self.page.query_selector("textarea")
            if textarea:
                textarea.fill(content)
                time.sleep(1)
            
            # Якщо є зображення, додати його
            if image_url:
                logger.info(f"Adding image: {image_url}")
                # TODO: Реалізація завантаження зображення
            
            # Натиснути "Post"
            post_button = self.page.query_selector(
                "button:has-text('Post'):not(:disabled)"
            )
            
            if not post_button:
                logger.error("Could not find 'Post' button")
                return False
            
            post_button.click()
            
            # Очікування завантаження
            time.sleep(3)
            
            logger.info("✅ LinkedIn post published successfully")
            return True
        
        except Exception as e:
            logger.error(f"❌ LinkedIn publish error: {e}")
            return False
        
        finally:
            # Закриття браузера
            if self.browser:
                self.browser.close()
                self.browser = None
                self.page = None
    
    def close(self) -> None:
        """Закриває браузер та очищує ресурси."""
        if self.browser:
            self.browser.close()
            self.browser = None
            self.page = None
            logger.info("LinkedIn browser closed")
