import datetime
import os
import sqlite3

from flask import Flask, render_template, url_for, request, flash, get_flashed_messages, g, abort, \
    make_response, redirect, session
from flask_migrate import Migrate

from flask_006.admin.admin import admin
from flask_006.flask_database import FlaskDataBase
from werkzeug.security import generate_password_hash, check_password_hash

from flask_006.helpers import check_ext
from flask_006.models import db, User, Profile, News

DATABASE = 'main.db'
DEBUG = True
SECRET_KEY = 'gheghgj3qhgt4q$#^#$he'
MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
app.permanent_session_lifetime = datetime.timedelta(days=1)

app.register_blueprint(admin, url_prefix='/admin')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# postgres://user:password@localhost/database_name

db.init_app(app)
migrate = Migrate(app, db)

upload_files_dir = 'uploads'


def create_db():
    """Creates new database from sql file."""
    db_raw = connect_db()
    with app.open_resource('db_schema.sql', mode='r') as f:
        db_raw.cursor().executescript(f.read())
    db_raw.commit()
    db_raw.close()


def connect_db():
    """Returns connention to apps database."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


url_menu_items = {
    'index': 'Главная',
    'second': 'Вторая страница'
}


@app.before_first_request
def before_first_request_func():
    print('BEFORE_FIRST REQUEST called!')


fdb = None
db_raw = None


@app.before_request
def before_request_func():
    global fdb
    global db_raw
    db_raw = get_db()
    fdb = FlaskDataBase(db_raw)
    print('BEFORE REQUEST called!')


@app.after_request
def after_request_func(response):
    print('AFTER REQUEST called!')
    return response


@app.teardown_request
def teardown_request_func(response):
    print('TEARDOWN REQUEST called!')
    return response


@app.teardown_appcontext
def close_db(error):
    """Close database connection if it exists."""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    user = User.query.first()
    return render_template(
        'index.html',
        menu_url=fdb.get_menu(),
        posts=fdb.get_posts()
    )


@app.route('/page2')
def second():
    print(url_for('second'))
    print(url_for('index'))

    return render_template(
        'second.html',
        phone='+79172345678',
        email='myemail@gmail.com',
        current_date=datetime.date.today().strftime('%d.%m.%Y'),
        menu_url=fdb.get_menu()
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        try:
            hash = generate_password_hash(request.form['password'])
            user = User(
                email=request.form['email'],
                password=hash
            )
            db.session.add(user)
            db.session.flush()

            profile = Profile(
                name=request.form['name'],
                birthdate=datetime.date.fromisoformat(request.form['birthdate']),
                city=request.form['city'],
                user_id=user.id
            )
            db.session.add(profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Exception while creating user: {e}')
        return redirect(url_for('index'))


# int, float, path
@app.route('/user/<username>')
def profile(username):
    return f"<h1>Hello {username}!</h1>"


@app.route('/add_post', methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        name = request.form["name"]
        post_content = request.form["post"]
        file = request.files.get('file')
        img = None
        if len(name) > 5 and len(post_content) > 10:
            if file and check_ext(file.filename):
                try:
                    img = file.read()
                except FileNotFoundError:
                    flash('Ошибка чтения файла', category='error')
                    img = None
            res = fdb.add_post(name, post_content, img)
            if not res:
                flash('Post were not added. Unexpected error', category='error')
            else:
                flash('Success!', category='success')
        else:
            flash('Post name or content too small', category='error')

    return render_template('add_post.html', menu_url=fdb.get_menu())


@app.route('/post/<int:post_id>')
def post_content(post_id):
    title, content = fdb.get_post_content(post_id)
    if not title:
        abort(404)
    return render_template('post.html', menu_url=fdb.get_menu(), title=title, content=content)


@app.route('/photo/<int:post_id>')
def post_photo(post_id):
    photo = fdb.get_post_photo(post_id)
    response = make_response(photo)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/ajax', methods=['GET', 'POST'])
def ajax_example():
    if request.method == 'POST':
        number_value = request.form.get('number', 0) or 0
        number = int(number_value)
    else:
        number_value = request.args.get('number', 0) or 0
        number = int(number_value)
    return f'{number + 1}'


@app.route('/ajax_items', methods=['POST'])
def ajax_items():
    items = {
        1: 'iPhone 13 Pro',
        2: 'Macbook pro 16"',
        3: 'Xiaomi airdots 2 pro ultra',
        4: 'Dyson стайлер'
    }
    return items


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', menu_url=fdb.get_menu())
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email:
            flash('Email не указан!', category='unfilled_error')
        elif '@' not in email or '.' not in email:
            flash('Некорректный email!', category='validation_error')
        elif not password:
            flash('Пароль не указан!', category='unfilled_error')
        else:
            if password == '12345':
                return redirect(url_for('index'))

        print(get_flashed_messages(True))
        return render_template('login.html', menu_url=fdb.get_menu())
    else:
        raise Exception(f'Method {request.method} not allowed')


@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Ooooops! This post does not exist!</h1>"


@app.route('/test_response1')
def test_response():
    content = render_template(
        'index.html',
        menu_url=fdb.get_menu(),
        posts=fdb.get_posts()
    )
    response_obj = make_response(content)
    response_obj.headers['Content-type'] = 'text/plain'
    return response_obj


@app.route('/test_response2')
def test_response2():
    return "<h1>Test response 2 page</h1>", 404, {'Content-Type': 'text/plain'}


@app.route('/redirect')
def redirect_example():
    return redirect(url_for('index')), 301


@app.route('/test_login')
def test_login():
    log = ''
    if request.cookies.get('visited'):
        log = request.cookies.get('visited')

    response = make_response(f"<h1>Visited cookie: {log}</h1>")
    response.set_cookie('visited', 'yes')
    return response

@app.route('/test_login1')
def test_login1():
    log = ''
    if request.cookies.get('visited'):
        log = request.cookies.get('visited')

    response = make_response(f"<h1>Visited cookie: {log}</h1>")
    response.delete_cookie('visited')
    return response


@app.route('/session_example')
def session_example():
    if 'visits' in session:
        session['visits'] += 1
    else:
        session['visits'] = 1

    return f"<h1>Number of visits: {session['visits']}</h1>"


@app.route('/session_example2')
def session_example2():
    counter = session.get('visits', 1)
    session['visits'] = counter + 1
    return f"<h1>Number of visits: {session['visits']}</h1>"


data = [1, 2, 3]


@app.route('/session_example3')
def session_example3():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][0] += 1
        session.modified = True
    return f"<h1>Data: {session['data']}</h1>"


@app.route('/hash_example')
def hash_example():
    password = 'Password12345'
    hash = generate_password_hash(password)

    print(check_password_hash(hash, 'Password1234'))
    return f"<h1>Hash: {hash}</h1>"


@app.route('/news')
def news_list():
    news = News.query.all()
    return render_template('news.html', menu_url=fdb.get_menu(), news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == "POST":
        try:
            upload_file = request.files.get('photo')
            # upload_files = request.files.getlist("photo")
            file_path = None
            if upload_file:
                file_ext = upload_file.filename.rsplit('.', 1)[1]
                file_path = os.path.join(
                    upload_files_dir,
                    f"{generate_password_hash(upload_file.filename)}.{file_ext}"
                )
                upload_file.save(os.path.join('static', file_path))
            news = News(
                title=request.form['title'],
                content=request.form['content'],
                photo=file_path,
                pub_date=datetime.datetime.now()
            )
            db.session.add(news)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Exception while adding news: {e}")
        return redirect(url_for('news_list'))
    return render_template('add_news.html')


if __name__ == '__main__':
    app.run(debug=True)
