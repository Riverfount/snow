from business_rules import add_new_post, get_posts_from_database
from snow import Snow

app = Snow()


@app.route('^/$', template='list.template.html')
def post_list():
    posts = get_posts_from_database()
    return {'post_list': posts}


@app.route('^/api$')
def post_list_api():
    posts = get_posts_from_database()
    return {'post_list': posts}, '200 OK', 'application/json'


@app.route(r'^/(?P<post_id>\d{1,}$)', template='post.template.html')
def post_detail(post_id):
    post = get_posts_from_database(post_id=post_id)[0]
    return {'post': post}


@app.route('^/new$', template='form.template.html')
def new_post_form():
    return {}


@app.route('^/new$', method='POST')
def new_post_add(form):
    post = {item.name: item.value for item in form.list}
    add_new_post(post)
    return "New post Created with Success", '201 Created', 'text/plain'


if __name__ == '__main__':
    app.run()
