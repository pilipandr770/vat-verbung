# HOW_TO_RUN — Запуск проєкту

## Передумови

- Python 3.9+
- PostgreSQL 12+
- Облікові записи на LinkedIn, Telegram, Instagram

---

## Крок 1: Встановлення

```bash
# Клонування / розпакування проєкту
cd promotion_hub

# Встановлення залежностей
pip install -r requirements.txt

# (Опціонально) Віртуальне середовище
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

---

## Крок 2: БД

### Створення БД

```bash
psql -U postgres

CREATE DATABASE promotion_hub;
CREATE SCHEMA promotion_hub;
```

### Ініціалізація таблиць

```sql
-- Таблиця лідів
CREATE TABLE promotion_hub.leads (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50),
    platform VARCHAR(50),
    identifier VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    username VARCHAR(255),
    bio TEXT,
    score FLOAT DEFAULT 0.0,
    invited BOOLEAN DEFAULT False,
    blocked BOOLEAN DEFAULT False,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблиця постів
CREATE TABLE promotion_hub.posts (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    content_de TEXT,
    content_adapted TEXT,
    language VARCHAR(10) DEFAULT 'de',
    published BOOLEAN DEFAULT False,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблиця дій
CREATE TABLE promotion_hub.actions (
    id SERIAL PRIMARY KEY,
    action_type VARCHAR(50),
    channel VARCHAR(50),
    lead_id INTEGER REFERENCES promotion_hub.leads(id),
    post_id INTEGER REFERENCES promotion_hub.posts(id),
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблиця логів
CREATE TABLE promotion_hub.logs (
    id SERIAL PRIMARY KEY,
    message TEXT,
    level VARCHAR(20) DEFAULT 'INFO',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Крок 3: Конфігурація

### Скопіюйте .env.example → .env

```bash
cp .env.example .env
```

### Відредагуйте .env

```env
# DATABASE
DATABASE_URL=postgresql://user:password@localhost:5432/promotion_hub
DB_SCHEMA=promotion_hub

# LinkedIn
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
# Отримайте токен: https://www.linkedin.com/developers/

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=-your_channel_id
# Отримайте: https://t.me/BotFather

# Instagram
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
# УВАГА: Використовуйте app-specific password для безпеки

# Налаштування
DEBUG=False
LOG_LEVEL=INFO
```

---

## Крок 4: Запуск

### Режим розробки (один раз)

```bash
python main.py
```

Scheduler запуститься і почне:
1. Генерувати контент
2. Публікувати пости
3. Збирати лідів
4. Запрошувати релевантних людей

### Режим виробництва (background)

```bash
# Linux / Mac
nohup python main.py > promotion_hub.log 2>&1 &

# Windows (PowerShell)
Start-Process python main.py -WindowStyle Hidden

# Або як service (systemd)
sudo systemctl start promotion-hub
```

---

## Крок 5: Моніторинг

### Перевірка логів

```bash
# Live logs
tail -f promotion_hub.log

# PostgreSQL logs
SELECT * FROM promotion_hub.logs ORDER BY created_at DESC LIMIT 10;

# Статистика
SELECT 
    COUNT(*) as total_leads,
    COUNT(CASE WHEN invited THEN 1 END) as invited,
    COUNT(CASE WHEN blocked THEN 1 END) as blocked
FROM promotion_hub.leads;
```

### Сигнали

```
✅ INFO: "Cycle executed successfully"
⚠️ WARNING: "Daily limit reached for telegram"
❌ ERROR: "Failed to publish post"
```

---

## Усунення проблем

### Проблема: "Connection refused" для БД

```bash
# Перевіріть PostgreSQL
sudo systemctl status postgresql

# Перевіріть .env
echo $DATABASE_URL
```

### Проблема: "Invalid LinkedIn token"

```bash
# Токен потребує оновлення
# Перейдіть на https://www.linkedin.com/developers/
# Сгенеруйте новий токен і оновіть .env
```

### Проблема: Telegram API rate limit

```
Scheduler автоматично спускає затримку між запрошеннями
Перевіріть RULES.md для лімітів
```

---

## Команди для тестування

```bash
# Тест підключення до БД
python -c "from core.models import *; print('DB OK')"

# Тест генерації контенту
python -c "from core.content_engine import ContentEngine; \
           e = ContentEngine(); \
           print(e.generate_content('risks'))"

# Тест адаптації контенту
python -c "from core.content_adapter import ContentAdapter; \
           a = ContentAdapter(); \
           print(a.adapt('Test content', 'telegram'))"
```

---

## Безпека

- 🔒 **Ніколи не комітьте .env**
- 🔒 **Використовуйте strong passwords**
- 🔒 **Оновлюйте залежності**: `pip install --upgrade -r requirements.txt`
- 🔒 **Регулярно перевіряйте логи на аномалії**

---

## Підтримка

Якщо щось не працює:
1. Перевірте логи: `tail -f promotion_hub.log`
2. Перевірте конфіг: `.env`
3. Перевірте БД: `psql -l`
4. Перевірте API tokens (мають ви поточні?)

Happy promoting! 🚀
