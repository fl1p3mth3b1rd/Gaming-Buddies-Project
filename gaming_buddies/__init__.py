from flask import Flask, render_template
from gaming_buddies.model import db, GameInformation


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    @app.route('/')
    def index():
        title = 'Главная страница'
        game_list = GameInformation.query.all()
        print(type((game_list[1])))
        return render_template('index.html', title=title, game_list=game_list)
    return app

