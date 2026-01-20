# ARCHITECTURE — Архітектура Promotion Hub

## Загальна схема

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│              (єдина точка входу)                    │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │   core/scheduler.py     │
         │   (оркестратор)         │
         └─────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    LinkedIn      Telegram      Instagram
   (Publisher)  (Collector +  (Collector +
                Analyzer +    Analyzer +
                Inviter +     Inviter +
                Publisher)    Publisher)
```

## Шари

### 1. Core (ядро)

**content_engine.py**
- Генерує базовий контент німецькою (DE)
- Теми: ризики, довіра, автоматизація, операційка
- Один контент для всіх каналів

**content_adapter.py**
- Адаптує контент під платформу
- LinkedIn: довгий, професійний
- Telegram: коротко, з emoji
- Instagram: візуальна, з hashtags

**scheduler.py**
- Оркеструє цикли публікацій
- Запускає збір ЦА
- Запускає запрошення

**scoring.py**
- Оцінює релевантність лідів
- Визначає: SAVE / INVITE / SKIP

**rules.py**
- Антиспам-правила
- Ліміти на день
- Затримки між діями
- Не більше 1 запрошення на людину

**models.py**
- Моделі БД (Lead, Post, Action)
- Інтеграція з PostgreSQL

### 2. Channels (канали)

Кожен канал незалежний і містить:
- **collector.py** — збір ЦА
- **analyzer.py** — аналіз релевантності
- **inviter.py** — запрошення/контакт
- **publisher.py** — публікація
- **README.md** — правила каналу

## Потік даних

```
Content Engine (DE) 
    ↓
Content Adapter (Platform-specific)
    ↓
Scheduler (коли публікувати?)
    ↓
Publisher (LinkedIn / Telegram / Instagram)
    ↓
Collector (збір ЦА)
    ↓
Analyzer (оцінка релевантності)
    ↓
Scoring (SAVE / INVITE / SKIP)
    ↓
Rules Engine (антиспам проверка)
    ↓
Inviter (запрошення)
    ↓
PostgreSQL (логування всього)
```

## Бази даних

### PostgreSQL schema: promotion_hub

**leads**
- id, platform, identifier, email, username
- bio, score, invited, created_at

**posts**
- id, channel, content_de, content_adapted
- published, published_at

**actions**
- id, action_type, channel, lead_id, post_id
- details, created_at

**logs**
- id, message, level, created_at

## Безпека

- Немає public API ендпоінтів
- Усі ключі у .env
- Жодного спаму (антиспам-правила)
- Логування всіх дій

## Масштабування

Проєкт готовий до:
- Додавання нових тем контенту
- Додавання нових каналів (YouTube, TikTok)
- Інтеграції з CRM
- Розширення аналізу (ML для scoring)
