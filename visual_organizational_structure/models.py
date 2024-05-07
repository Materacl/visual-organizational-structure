from flask_login import UserMixin
import jwt
import datetime

from visual_organizational_structure import db, manager
from flask import current_app as app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dashboards = db.relationship('Dashboard', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1200):
        reset_token = jwt.encode(
            {
                'user': self.id,
                'exp': datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        return User.query.get(data.get('user'))


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    graph_data = db.Column(db.Text, nullable=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
