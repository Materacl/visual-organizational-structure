from flask_login import UserMixin

from main_app import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dashboards = db.relationship('Dashboard', backref='user', lazy=True)


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
