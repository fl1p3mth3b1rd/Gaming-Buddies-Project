from getpass import getpass
import sys

from gaming_buddies import create_app
from gaming_buddies.model import db, UserGeneralInformation

app = create_app()

with app.app_context():
    nickname = input('Введите имя:')

    if UserGeneralInformation.query.filter(UserGeneralInformation.nickname == nickname).count():
        print('Пользователь с таким именем уже существует')
        sys.exit(0)

    password1 = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2:
        print('Пароль не совпадают')
        sys.exit(0)

    new_user = UserGeneralInformation(nickname=nickname, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
    