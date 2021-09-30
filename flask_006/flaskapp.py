import datetime

from flask import Flask, render_template, url_for, request, flash, get_flashed_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gheghgj3qhgt4q$#^#$he'

url_menu_items = {
    'index': 'Главная',
    'second': 'Вторая страница'
}


@app.route('/')
def index():
    return render_template('index.html', menu_url=url_menu_items)


@app.route('/page2')
def second():
    menu_items = [
        'Главная',
        'Каталог',
        'Доставка',
        'О компании',
    ]

    print(url_for('second'))
    print(url_for('index'))

    return render_template(
        'second.html',
        phone='+79172345678',
        email='myemail@gmail.com',
        current_date=datetime.date.today().strftime('%d.%m.%Y'),
        menu=menu_items,
        menu_url=url_menu_items
    )


# int, float, path
@app.route('/user/<username>')
def profile(username):
    return f"<h1>Hello {username}!</h1>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', menu_url=url_menu_items)
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email:
            flash('Email не указан!', category='unfilled_error')
        else:
            if '@' not in email or '.' not in email:
                flash('Некорректный email!', category='validation_error')
        if not password:
            flash('Пароль не указан!', category='unfilled_error')

        print(request)
        print(get_flashed_messages(True))
        return render_template('login.html', menu_url=url_menu_items)
    else:
        raise Exception(f'Method {request.method} not allowed')


if __name__ == '__main__':
    app.run(debug=True)
