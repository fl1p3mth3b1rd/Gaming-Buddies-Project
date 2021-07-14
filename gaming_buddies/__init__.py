
from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_login.utils import logout_user
from gaming_buddies.model import db, UserGeneralInformation, GameInformation, Post
from gaming_buddies.forms import LoginForm, RegistrationForm, LookingForGamersForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return UserGeneralInformation.query.get(user_id)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = UserGeneralInformation.query.filter_by(nickname=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/registration')
    def registration():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Регистрация'
        reg_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=reg_form)
    
    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = UserGeneralInformation(nickname=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
            return redirect(url_for('register'))

    @app.route('/post/<int:game_id>')
    def post(game_id):
        title = 'Поиск игроков'
        form = LookingForGamersForm()
        return render_template('application.html', page_title=title, form=form, game_id=game_id)
    
    @app.route('/process-post/<int:game_id>', methods=['POST'])
    @login_required
    def process_post(game_id):
        user_id = current_user.get_id()
        user_object = UserGeneralInformation.query.filter(UserGeneralInformation.id==user_id).first()
        game_object = GameInformation.query.filter(GameInformation.game_id==game_id).first()
        form = LookingForGamersForm()
        if form.validate_on_submit():
            new_post = Post(country=form.country.data, 
                timezone=form.time_zone.data,
                description_as_author=form.description_as_author.data,
                purpose_as_author=form.purpose_as_author.data,
                discord=form.discord.data,
                prime_time=form.prime_time.data,
                user_post=user_object,
                game_linked_post=game_object)
            db.session.add(new_post)
            db.session.commit()
            flash('Спасибо за пост!')
            return redirect(url_for('single_game', game_id=game_id))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
            return redirect(request.referrer)

    @app.route('/')
    def index():
        title = 'Поиск игр'
        game_list = GameInformation.query.all()
        number_of_games = len(game_list)
        number_of_posts = db.session.query(Post).count()
        return render_template('index.html', title=title, game_list=game_list, number_of_games=number_of_games, number_of_posts=number_of_posts)

    @app.route('/<int:game_id>')
    def single_game(game_id):
        game = GameInformation.query.filter(GameInformation.game_id == game_id).first()
        posts = Post.query.filter(Post.linked_game_id == game_id).all()
        if not game:
            abort(404)
        return render_template('single_game.html', page_title=game.name, game=game, posts=posts)

    @app.route('/<int:game_id>/<int:post_id>')
    def post_page(game_id, post_id):
        post_author_id = Post.query.filter(Post.post_id == post_id).first().user_id
        post_aurhor_nickname = UserGeneralInformation.query.filter(UserGeneralInformation.id == post_author_id).first().nickname
        title = "Предложение для совместной игры"
        post = Post.query.filter(Post.post_id==post_id).first()
        return render_template('single_post.html', page_title=title, post=post, post_aurhor_nickname=post_aurhor_nickname)

    @app.route('/test')
    def user_profile():
        return render_template('user_profile.html')
    
    @app.route('/test2')
    def test_template2():
        return render_template('test2.html')
    
    return app

