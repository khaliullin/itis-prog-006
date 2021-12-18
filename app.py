from flask import Flask, render_template
from flask_migrate import Migrate

from models import db, User

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db:5432/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"


@app.route('/db')
def db_user():
    user = User.query.first()
    return render_template(
        "index.html",
        user=user
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
