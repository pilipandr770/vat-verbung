# Promotion Hub v1.0 🚀

**B2B Marketing Automation Platform** для автоматизации маркетинга в LinkedIn, Instagram та Telegram німецькою мовою.

## ⚡ Quick Start

### 1️⃣ Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 2️⃣ Налаштування конфігурації
```bash
# Скопіюй шаблон
cp .env.example .env

# Заповни свої дані в .env
# - DATABASE_URL (PostgreSQL)
# - LINKEDIN_USERNAME / LINKEDIN_PASSWORD
# - TELEGRAM_BOT_TOKEN / TELEGRAM_CHANNEL_ID
# - INSTAGRAM_USERNAME / INSTAGRAM_PASSWORD
```

### 3️⃣ Ініціалізація Instagram сесії
```bash
python init_instagram.py
```

### 4️⃣ Запуск системи
```bash
# Windows
run.bat

# Linux / macOS
bash run.sh

# або безпосередньо
python main.py
```

## 📋 Компоненти

### Core Модули (`core/`)
- **models.py** - PostgreSQL ORM для Lead, Post, Action, Log
- **db_init.py** - Ініціалізація БД схеми та таблиць
- **scheduler.py** - APScheduler оркестратор (10+ job'ів)
- **content_engine.py** - 4 тематики × 4 типи контенту (64+ варіантів)
- **content_adapter.py** - Адаптація контенту для кожного каналу
- **scoring.py** - B2B скоринг лідів (27 ключових слів)
- **rules.py** - Правила і обмеження (1 інвайт на ліда, денні ліміти)

### Канали (`channels/`)
- **Instagram** - Collector, Analyzer, Inviter, Publisher
- **Telegram** - Collector (framework), Analyzer, Inviter, Publisher
- **LinkedIn** - Publisher (Playwright automation)

### Утиліти
- **system_check.py** - Перевірка конфігурації перед запуском
- **init_instagram.py** - Ініціалізація Instagram сесії
- **test_instagram.py** - Перевірка Instagram з'єднання
- **run.bat** / **run.sh** - Стартові скрипти

## 🎯 Розклад Jobs

| Канал | Частота | Час |
|-------|---------|--------|
| **LinkedIn** | 2x на день | 08:00, 15:00 |
| **Instagram** | 3x на день | 09:00, 13:00, 19:00 |
| **Telegram** | 5x на день | 08:00, 11:00, 14:00, 17:00, 20:00 |
| **Збір лідів** | Кожні 6-8 годин | - |
| **Інвайти** | Кожні 2-3 години | - |

## 🔒 Безпека

✅ Усі credentials в `.env` (в `.gitignore`)  
✅ Instagram сесія зберігається локально  
✅ Database connection pooling  
✅ Логування всіх дій в БД  
✅ Затримки між actions (уникнення блокувань)  

## 📊 Моніторинг

### Логи
```bash
# Real-time логи (Linux/Mac)
tail -f logs/promotion_hub.log

# Останні 100 рядків
tail -100 logs/promotion_hub.log
```

### База даних
```sql
-- Останні actions
SELECT * FROM promotion_hub.actions 
WHERE created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- Статистика лідів
SELECT source, COUNT(*) as total, 
  COUNT(*) FILTER (WHERE invited) as invited,
  AVG(score) as avg_score
FROM promotion_hub.leads
GROUP BY source;

-- Логи системи
SELECT message, level, created_at 
FROM promotion_hub.logs
ORDER BY created_at DESC
LIMIT 50;
```

## 🔧 Troubleshooting

### Instagram: "Session may have expired"
```bash
# Переінціалізуй сесію
python init_instagram.py
```

### Database: "Connection refused"
- Перевір `DATABASE_URL` в `.env`
- Переконайся що PostgreSQL запущена
- Перевір credentials

### Telegram: "Bot token invalid"
- Отримай новий токен від @BotFather
- Використовуй формат: `123456789:ABCDEFGHIJKLMNOPQRSTUVWxyz...`

### LinkedIn: "Login failed"
- Перевір username/password
- Можлива блокування (спробуй пізніше)
- Переконайся що це не робочий аккаунт (потрібна верифікація)

## 📈 Розширення

Готові до реалізації:
- YouTube інтеграція
- Email кампанії
- TikTok/Pinterest
- ML-based скоринг
- Analytics dashboard
- CRM інтеграція

## 📝 Ліцензія

Internal Use Only - Do Not Distribute

## 👥 Підтримка

Для питань і проблем:
1. Перевір `logs/promotion_hub.log`
2. Запусти `python system_check.py`
3. Перевір документацію в `docs/`

---

**Готово до production!** 🎉 Запусти `python main.py` або `run.bat`
