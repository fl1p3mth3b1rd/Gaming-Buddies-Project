from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_general_information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20))
    # profile_photo = 

    def __repr__(self):
        return "<User id: {}, User nickname {}>".format(self.id, self.nickname)
