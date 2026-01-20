# README — Promotion Hub

Внутрішній B2B-маркетинговий інструмент для просування проєкту.

## Швидкий старт

```bash
# 1. Установка залежностей
pip install -r requirements.txt

# 2. Налаштування змінних середовища
cp .env.example .env
# відредагуйте .env з вашими даними

# 3. Запуск
python main.py
```

## Структура

- **core/** — основні модулі (контент-двигун, оркестратор, правила)
- **channels/** — незалежні канали (LinkedIn, Telegram, Instagram)
- **docs/** — документація
- **data/** — службові файли

## Принципи

✅ Один контент-завод  
✅ Три незалежні канали  
✅ Персоналізований пошук ЦА  
✅ Одне запрошення на людину  
✅ Жодного спаму  
✅ Усе логується в БД  

## Документація

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — архітектура
- [CHANNELS.md](docs/CHANNELS.md) — деталі каналів
- [CONTENT_STRATEGY.md](docs/CONTENT_STRATEGY.md) — контент-стратегія
- [RULES.md](docs/RULES.md) — антиспам-правила
- [HOW_TO_RUN.md](docs/HOW_TO_RUN.md) — запуск

## Ліцензія

Приватний проєкт.
