import os
import re
from flask import Flask, render_template, flash, redirect, url_for, abort, request, current_app
from flask_login.utils import logout_user
# from sqlalchemy.orm import session
from gaming_buddies.model import db, UserGeneralInformation, GameInformation, Post
from gaming_buddies.forms import LoginForm, RegistrationForm, LookingForGamersForm, AdditionalUserInformationForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    admin = Admin(app)
    admin.add_view(ModelView(GameInformation, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(UserGeneralInformation, db.session))

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    def allowed_profile_picture(filename):
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @app.route('/process-profile-picture-upload/<int:user_id>', methods=['POST'])
    @login_required
    def process_profile_picture_upload(user_id):
        if request.method == 'POST':
            if 'file' not in request.files:
                print('первый if')
                print(request.files)
                flash('Выберите файл')
                return redirect(request.referrer)
            file = request.files['file']
            if file.filename == '':
                print('второй if')
                flash('Выберите файл')
                return redirect(request.referrer)
            if file and allowed_profile_picture(file.filename):
                print('третий if')
                filename = f'user_{user_id}_pp.jpg'
                actual_directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                directory = "/static/profile_pictures/" + filename
                file.save(actual_directory)
                db.session.query(UserGeneralInformation).filter(UserGeneralInformation.nickname==
                    current_user.nickname).update(
                        {UserGeneralInformation.profile_picture_dir : directory})
                db.session.commit()
                flash('Изменения внесены')
                return redirect(url_for('edit_user_profile', user_id=user_id, name=filename))
            else:
                flash('Некорректный формат файла')
                return redirect(request.referrer)

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
            user = UserGeneralInformation.query.filter(UserGeneralInformation.nickname==form.username.data).first()
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
        username_check = UserGeneralInformation.query.filter(UserGeneralInformation.nickname==form.username.data).first()
        email_check = UserGeneralInformation.query.filter(UserGeneralInformation.email==form.email.data).first()
        if form.validate_on_submit():
            if username_check:
                flash('Имя пользователя занято')
                return redirect(request.referrer)
            if email_check:
                flash('Данный email уже зарегестрирован')
                return redirect(request.referrer)
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
            return redirect(url_for('registration'))

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

    @app.route('/', methods=['GET'])
    def index():
        title = 'Поиск игр'
        game_types_list = db.session.query(GameInformation.genre).distinct()
        number_of_posts = db.session.query(Post).count()
        print(request.url)
        print(request.args)
        if request.method == 'GET':
            if not request.args.get('game_searched') and request.args.get('genre_searched'):
                game_list = GameInformation.query.filter(GameInformation.genre ==
                    request.args['genre_searched']).all()
            elif request.args.get('game_searched') and not request.args.get('genre_searched'):
                game_list = GameInformation.query.filter(
                    GameInformation.proper_name.contains(request.args['game_searched'].lower())).all()
            elif request.args.get('game_searched') and request.args.get('genre_searched'):
                game_list = GameInformation.query.filter(GameInformation.proper_name.contains(
                    request.args['game_searched'].lower()), GameInformation.genre ==request.args['genre_searched']).all()
            else:
                game_list = GameInformation.query.all()
            number_of_games = len(game_list)
            return render_template('index.html', title=title, game_list=game_list, number_of_games=number_of_games,
            number_of_posts=number_of_posts, game_types_list=game_types_list)
        game_list = GameInformation.query.all()
        number_of_games = len(game_list)
        number_of_posts = db.session.query(Post).count()
        return render_template('index.html', title=title, game_list=game_list, number_of_games=number_of_games,
            number_of_posts=number_of_posts, game_types_list=game_types_list)

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return admin
        else:
            return 'Страница доступна только администраторам'

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
        return render_template('single_post.html', page_title=title, post=post, post_aurhor_nickname=post_aurhor_nickname,
            post_author_id=post_author_id)

    @app.route('/user_profile/<int:user_id>')
    @login_required
    def user_profile(user_id):
        user_object = UserGeneralInformation.query.filter(UserGeneralInformation.id==user_id).first()
        return render_template('user_profile.html', user_id=user_id, user_object=user_object)

    @app.route('/edit/user_profile')
    def edit_user_profile():
        form = AdditionalUserInformationForm()
        return render_template('edit_user_profile.html', form=form)

    @app.route('/process-edit/user_profile', methods=['POST'])
    @login_required
    def process_edit_user_profile():
        user_params = ['nickname','first_name', 'second_name', 'birth_date', 'gender', 'about_myself']
        form = AdditionalUserInformationForm()
        old_username = current_user.nickname
        new_nickname = form.nickname.data
        username_check = UserGeneralInformation.query.filter(UserGeneralInformation.nickname==new_nickname).first()
        if form.validate_on_submit():
            if username_check and new_nickname != old_username:
                flash('Пользователь с таким никнеймом уже существует')
                return redirect(request.referrer)
            else:
                params_to_update = {getattr(UserGeneralInformation, attr) : getattr(form, attr).data
                    for attr in user_params if getattr(form, attr).data}
                db.session.query(UserGeneralInformation).filter(UserGeneralInformation.nickname==old_username).\
                    update(params_to_update)
                db.session.commit()
                flash('Изменения внесены')
                return redirect(request.referrer)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
            return redirect(request.referrer)

    @app.route('/test2')
    def test_template2():
        return render_template('test2.html')

    @app.route('/test2_recieve', methods=['POST', 'GET'])
    def test_template2_recieve():
        print(request.form)
        return render_template('test2.html')

    return app

