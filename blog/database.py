from sqlite3 import connect

conn = connect('db.sqlite3')
cursor = conn.cursor()

conn.execute(
    '''\
    CREATE TABLE if not exists post (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        content varchar NOT NULL,
        author varchar NOT NULL
    );
    '''
)

posts = [
    {
        'title': 'Python é a melhor linguagem do mundo',
        'content': '''\
        A linguagem Python foi eleita a melhor e mais popular linguagem do mundo pela revista Hacker! 
        ''',
        'author': 'Satoshi Namamoto'
     },
    {
        'title': 'Como criar um blod utiliznado Python',
        'content': '''\
        Neste tutorial vc aprenderá como criar um blog utilizando Python.
        <pre>import make_a_blog</pre>
        ''',
        'author': 'Guido von Rossum'
    }
]

count = cursor.execute('SELECT * FROM post;').fetchall()
if not count:
    cursor.executemany(
        '''INSERT INTO post (title, content, author) VALUES (:title, :content, :author)''',
        posts,
    )
    conn.commit()

posts = cursor.execute('SELECT * FROM post').fetchall()
assert len(posts) >= 2

