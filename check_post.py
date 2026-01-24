from core.models import DatabaseConnection
db = DatabaseConnection()
with db.get_cursor() as cur:
    cur.execute('SELECT id, channel, content_de, published, published_at, created_at FROM posts WHERE id = 4')
    post = cur.fetchone()
    print('ПОДРОБНОСТИ ПОСЛЕДНЕГО ПОСТА:')
    print(f'ID: {post["id"]}')
    print(f'Канал: {post["channel"]}')
    print(f'Опубликован: {post["published"]}')
    print(f'Время публикации: {post["published_at"]}')
    print(f'Время создания: {post["created_at"]}')
    print(f'Заголовок: {post["content_de"][:100]}...')