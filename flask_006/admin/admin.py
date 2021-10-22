import sqlite3

from flask import Blueprint, request, redirect, url_for, session, render_template, flash, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return bool(session.get('admin_logged', False))


db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if is_logged():
        return render_template('admin/index.html')
    else:
        return redirect(url_for('.login'))


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Wrong username or password!', category='error')

    return render_template('admin/login.html')


@admin.route('/logout')
def logout():
    logout_admin()
    return redirect(url_for('.index'))


@admin.route('/posts')
def posts():
    if not is_logged():
        return redirect(url_for('.login'))

    posts = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, content FROM posts")
            posts = cur.fetchall()
        except sqlite3.Error as e:
            print(f'Exception: {e}')
    return render_template('admin/posts.html', posts=posts)
