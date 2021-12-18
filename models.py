from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"User {self.id} ({self.email})"
