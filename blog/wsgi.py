import cgi

from database import conn
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


def get_posts_from_database(post_id=None):
    cursor = conn.cursor()
    fields = ('id', 'title', 'content', 'author')
    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post;')
    posts = [dict(zip(fields, post)) for post in results]
    return posts


def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context).encode('utf-8')


def get_post_list(posts):
    post_list = [
        f'''<li><a href="/{post['id']}">{post['title']}</a></li>'''
        for post in posts
    ]
    return '\n'.join(post_list)


def add_new(post):
    cursor = conn.cursor()
    cursor.execute(
        '''\
        INSERT INTO post (title, content, author) VALUES (:title, :content, :author)
        ''',
        post
    )
    conn.commit()


def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    body = b'Content not found'
    status = '404 Not Found'

    if path == '/' and method == 'GET':
        posts = get_posts_from_database()
        body = render_template('list.template.html', post_list=posts)
        status = '200 OK'
    elif path.split('/')[-1].isdigit() and method == 'GET':
        post_id = path.split('/')[-1]
        body = render_template('post.template.html', post=get_posts_from_database(post_id)[0])
        status = '200 OK'
    elif path == '/new' and method == 'GET':
        body = render_template('form.template.html')
        status = '200 OK'
    elif path == '/new' and method == 'POST':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=1)
        post = {item.name: item.value for item in form.list}
        add_new(post)
        body = b'New post created successfully'
        status = '201 Created'

    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    server = make_server("127.0.0.1", 8000, application)
    print('Server is on line!')
    server.serve_forever()
