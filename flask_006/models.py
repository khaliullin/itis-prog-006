import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"user {self.id} ({self.email})"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date)
    city = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'profile {self.id}'


class Mainmenu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(128))

    def __repr__(self):
        return f'mainmenu {self.id} ({self.title})'


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    photo = db.Column(db.BLOB)
    pub_date = db.Column(db.Integer)

    def __repr__(self):
        return f'post {self.id}'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    photo = db.Column(db.String(256))
    pub_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'news {self.id}'
