from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from app import db, app
from time import time
import jwt
from flask_security import RoleMixin

role_user = db.Table('role_users',
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
                     )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=role_user, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # def has_role(self, role):
    #     role_id = Role.query.filter_by(name='role').first()
    #     # user_roles = role_user.query.filter_by(user_id=self.id).all()
    #     x = 2


    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_code = db.Column(db.String(140))
    size = db.Column(db.String(120), index=True)
    cloth = db.Column(db.String(50), index=True)
    sex = db.Column(db.String(10))
    type = db.Column(db.String(15), index=True)
    price = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Thing {}, {}, {}>'.format(self.type, self.sex, self.size)


#FLASK SICURITY




class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
