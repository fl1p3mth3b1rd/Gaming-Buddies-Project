import os

basedir = os.path.abspath(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'gaming_buddies.db')
SECRET_KEY = 'dkasjfjoj12pk3o12i3-ofui0rigfdpoq394u1309irfkdclvmzodiuf0932ro024tgk2i4wj0f9k,vpcovk2v94'
SQLALCHEMY_TRACK_MODIFICATIONS = False
GAME_LOGOS_DIRECTORY = os.path.join(basedir, '..', 'game_logos')