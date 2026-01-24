from core.models import DatabaseConnection
db = DatabaseConnection()
with db.get_cursor() as cur:
    cur.execute('SELECT id, content_de, content_adapted FROM posts WHERE published = TRUE ORDER BY published_at DESC LIMIT 1')
    post = cur.fetchone()
    print('ПОСЛЕДНИЙ ОПУБЛИКОВАННЫЙ ПОСТ:')
    print(f'ID: {post["id"]}')
    print()
    print('content_de:')
    print(repr(post['content_de']))
    print()
    print('content_adapted:')
    print(repr(post['content_adapted']))