from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template
from datetime import datetime
# from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_pyfile('config.py')

# naming_convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(column_0_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }
db = SQLAlchemy(app)

class UserGeneralInformation(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False, index=True, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20))
    posts = db.relationship('Post', backref='user_post')
    reg_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    responses = db.relationship('UserResponse', backref='user_response')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User id: {}, User nickname {}>".format(self.id, self.nickname)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_general_information.id', ondelete='CASCADE'))
    linked_game_id = db.Column(db.Integer, db.ForeignKey('game_information.game_id', ondelete='CASCADE'))
    country = db.Column(db.String(100))
    timezone = db.Column(db.String(50))
    description_as_author = db.Column(db.Text)
    purpose_as_author = db.Column(db.Text)
    discord = db.Column(db.String(50))
    prime_time = db.Column(db.String(50))
    post_status = db.Column(db.String(50))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    responses = db.relationship('UserResponse', backref='post_response')

class UserResponse(db.Model):
    response_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_general_information.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='CASCADE'))
    response_status = db.Column(db.String(30))

class GameInformation(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    linked_posts = db.relationship('Post', backref='game_linked_post')
    name = db.Column(db.String(200))
    genre = db.Column(db.String(200))
    game_logo_dir = db.Column(db.String(1000))
    def __repr__(self):
        return '<{} {}>'.format(self.name, self.genre)