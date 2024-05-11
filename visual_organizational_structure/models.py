from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

from visual_organizational_structure import db, manager
from flask import current_app as app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(127), unique=True, nullable=False)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dashboards = db.relationship('Dashboard', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    graph_data = db.Column(db.Text, nullable=True)
    raw_data = db.Column(db.Text, nullable=True)
    graph_paths = db.Column(db.Text, nullable=True)
    graph_roots = db.Column(db.Text, nullable=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
