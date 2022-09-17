from database import conn

cursor = conn.cursor()


def get_posts_from_database(post_id=None):
    fields = ('id', 'title', 'content', 'author')
    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post;')
    posts = [dict(zip(fields, post)) for post in results]
    return posts


def add_new_post(post):
    cursor.execute(
        '''\
        INSERT INTO post (title, content, author) VALUES (:title, :content, :author)
        ''',
        post
    )
    conn.commit()
