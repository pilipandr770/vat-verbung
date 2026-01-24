from core.content_generator import ContentGenerator
from core.content_engine import ContentEngine, ContentTopic, ContentType
from core.scheduler import Scheduler
import asyncio

async def test_full_workflow():
    # Генерация контента
    cg = ContentGenerator()
    content = cg.generate_content()
    print('📝 Контент сгенерирован')
    print(f'Длина: {len(content["description"])} символов')
    print(f'Тема: {content.get("theme", "unknown")}')

    # Генерация изображения через ContentEngine
    ce = ContentEngine()
    try:
        # Конвертируем тему в enum
        theme_str = content.get("theme", "compliance")
        topic_enum = ContentTopic(theme_str) if theme_str in [t.value for t in ContentTopic] else ContentTopic.COMPLIANCE
        content_type_enum = ContentType.PAIN  # По умолчанию

        image_path = ce.generate_image(
            topic_enum,
            content_type_enum,
            description=f"{content['title']} - {content['description'][:100]}"
        )
        print(f'🖼️ Изображение сгенерировано: {image_path}')
    except Exception as e:
        print(f'❌ Ошибка генерации изображения: {e}')
        image_path = None

    # Тестирование публикации через scheduler
    scheduler = Scheduler()
    try:
        # Запустим публикацию в Telegram (имитируем)
        scheduler._publish_telegram()
        print('✅ Публикация инициирована')
    except Exception as e:
        print(f'❌ Ошибка публикации: {e}')

if __name__ == "__main__":
    asyncio.run(test_full_workflow())