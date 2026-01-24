#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Анализ генерации контента
"""

from core.content_engine import ContentEngine, ContentTopic, ContentType

def main():
    print('📝 АНАЛИЗ ГЕНЕРАЦИИ КОНТЕНТА')
    print('=' * 60)

    ce = ContentEngine()

    print('🎨 ДОСТУПНЫЕ ТЕМЫ КОНТЕНТА:')
    for topic in ContentTopic:
        print(f'   • {topic.value}')

    print('\n📋 ТИПЫ КОНТЕНТА:')
    for ctype in ContentType:
        print(f'   • {ctype.value}')

    print('\n🔄 ПРИМЕРЫ ГЕНЕРАЦИИ ПО ТЕМАМ:')
    print('-' * 60)

    # Генерируем по каждой теме
    for topic in ContentTopic:
        content, _, ctype = ce.generate_content(topic=topic)
        print(f'\n🎯 Тема: {topic.value.upper()} ({ctype.value})')
        print(f'   "{content[:150]}..."')

    print('\n🤖 AI ГЕНЕРАЦИЯ VS STATIC:')
    print('-' * 60)

    # Проверяем AI генерацию
    if ce.ai_generator and ce.ai_generator.is_enabled():
        print('✅ AI генератор активен')

        # Пример AI генерации
        ai_result = ce.ai_generator.generate(ContentTopic.COMPLIANCE, ContentType.PAIN)
        if ai_result:
            ai_content, _, _ = ai_result
            print('\n🎨 AI сгенерированный контент:')
            print(f'   "{ai_content[:200]}..."')
        else:
            print('❌ AI генерация не удалась')
    else:
        print('⚠️  AI генератор не активен, используется static контент')

    print('\n📊 СТАТИСТИКА:')
    print(f'   Всего тем: {len(ContentTopic)}')
    print(f'   Всего типов: {len(ContentType)}')
    print(f'   Комбинаций: {len(ContentTopic) * len(ContentType)}')
    print(f'   Static контента: {len(ContentTopic) * len(ContentType) * 3} вариантов (3 на комбинацию)')

if __name__ == '__main__':
    main()