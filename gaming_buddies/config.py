import os

basedir = os.path.abspath(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'gaming_buddies.db')
