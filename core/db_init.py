"""
Ініціалізація схеми БД.
Запускається один раз при першому запуску.
"""

import os
import logging
import psycopg2
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


def init_database():
    """Ініціалізує схему та таблиці PostgreSQL."""
    database_url = os.getenv("DATABASE_URL")
    db_schema = os.getenv("DB_SCHEMA", "promotion_hub")
    
    if not database_url:
        raise ValueError("DATABASE_URL не встановлена в .env")
    
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    try:
        # 1. Створення схеми
        logger.info(f"Creating schema: {db_schema}")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {db_schema};")
        
        # 2. Встановлення search_path
        cur.execute(f"SET search_path TO {db_schema}, public;")
        
        # 3. Таблиця leads
        logger.info("Creating table: leads")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.leads (
                id SERIAL PRIMARY KEY,
                source VARCHAR(50) NOT NULL,
                platform VARCHAR(50) NOT NULL,
                identifier VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255),
                username VARCHAR(255),
                bio TEXT,
                score FLOAT DEFAULT 0.0,
                invited BOOLEAN DEFAULT FALSE,
                blocked BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 4. Таблиця posts
        logger.info("Creating table: posts")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.posts (
                id SERIAL PRIMARY KEY,
                channel VARCHAR(50) NOT NULL,
                content_de TEXT NOT NULL,
                content_adapted TEXT NOT NULL,
                language VARCHAR(10) DEFAULT 'de',
                published BOOLEAN DEFAULT FALSE,
                published_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 5. Таблиця actions
        logger.info("Creating table: actions")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.actions (
                id SERIAL PRIMARY KEY,
                action_type VARCHAR(50) NOT NULL,
                channel VARCHAR(50) NOT NULL,
                lead_id INTEGER REFERENCES {db_schema}.leads(id),
                post_id INTEGER REFERENCES {db_schema}.posts(id),
                details JSONB DEFAULT '{{}}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 6. Таблиця logs
        logger.info("Creating table: logs")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.logs (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                level VARCHAR(20) DEFAULT 'INFO',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 7. Індекси для оптимізації
        logger.info("Creating indexes")
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_leads_platform_identifier 
            ON {db_schema}.leads(platform, identifier);
        """)
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_leads_invited 
            ON {db_schema}.leads(invited);
        """)
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_actions_channel 
            ON {db_schema}.actions(channel);
        """)
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_logs_created_at 
            ON {db_schema}.logs(created_at DESC);
        """)
        
        conn.commit()
        logger.info(f"✅ Database initialized successfully in schema: {db_schema}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database()
