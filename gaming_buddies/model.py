from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserGeneralInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20))
    posts = db.relationship('Post_information', backref='user_post')
    responses = db.relationship('User_response', backref='user_response')

    def __repr__(self):
        return "<User id: {}, User nickname {}>".format(self.id, self.nickname)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_general_information.id'))
    country = db.Column(db.String(100))
    timezone = db.Column(db.String(50))
    description_as_author = db.Column(db.Text)
    purpose_as_author = db.Column(db.Text)
    discord = db.Column(db.String(50))
    prime_time = db.Column(db.String(50))
    post_status = db.Column(db.String(50))
    responses = db.relationship('User_response', backref='post_response')

class UserResponse(db.Model):
    response_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_general_information.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post_information.post_id'))
    response_status = db.Column(db.String(30))

class GameInformation(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    genre = db.Column(db.String(200))