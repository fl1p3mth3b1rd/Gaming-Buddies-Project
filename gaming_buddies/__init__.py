from flask import Flask, render_template, flash, redirect, url_for
from flask_login.utils import logout_user
from gaming_buddies.model import db, UserGeneralInformation
from gaming_buddies.forms import LoginForm, RegistrationForm, LookingForGamersForm
from flask_login import LoginManager, login_user, logout_user

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return UserGeneralInformation.query.get(user_id)

    @app.route('/login')
    def login():
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

    @app.route('logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        redirect(url_for('index'))

    @app.route('/registration')
    def registration():
        title = 'Регистрация'
        reg_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=reg_form)

    @app.route('/post')
    def post():
        title = 'Поиск игроков'
        post_form = LookingForGamersForm()
        return render_template('post.html', page_title=title, form=post_form)

    return app