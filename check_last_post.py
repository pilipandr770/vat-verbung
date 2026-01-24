from core.models import DatabaseConnection
db = DatabaseConnection()
with db.get_cursor() as cur:
    cur.execute('SELECT id, channel, content_de, published, published_at FROM posts WHERE id = 5')
    post = cur.fetchone()
    print('ПОСЛЕДНИЙ ПОСТ (ID 5):')
    print(f'Канал: {post["channel"]}')
    print(f'Опубликован: {post["published"]}')
    print(f'Время: {post["published_at"]}')
    print(f'Контент: {post["content_de"][:200]}...')