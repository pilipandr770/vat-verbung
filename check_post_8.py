from core.models import DatabaseConnection
db = DatabaseConnection()
with db.get_cursor() as cur:
    cur.execute('SELECT id, content_de, content_adapted FROM posts WHERE id = 8')
    post = cur.fetchone()
    print('КОНТЕНТ ПОСТА ID 8:')
    print('content_de:')
    print(repr(post['content_de']))
    print()
    print('content_adapted:')
    print(repr(post['content_adapted']))
    print()
    print('КОМБИНИРОВАННЫЙ ТЕКСТ (что отправляется в Telegram):')
    full_content = f"{post['content_de']}\n\n{post['content_adapted']}"
    print(repr(full_content))