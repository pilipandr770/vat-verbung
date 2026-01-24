from core.models import DatabaseConnection
db = DatabaseConnection()
with db.get_cursor() as cur:
    cur.execute('SELECT id, channel, content_de, content_adapted, published_at FROM posts WHERE id = 7')
    post = cur.fetchone()
    print('КОНТЕНТ ПОСТА ID 7:')
    print(f'Заголовок: {post["content_de"]}')
    print()
    print(f'Описание: {post["content_adapted"]}')
    print()
    print(f'Опубликовано: {post["published_at"]}')