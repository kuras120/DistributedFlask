import os
import logging

from ORM import db

from dotenv import load_dotenv

from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO

from Controllers.HomeController import home_controller
from Controllers.UserController import user_controller


def bind_blueprints(app):
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')


def init_env():
    if not os.path.isfile('.env'):
        file = open('.env', 'w+')
        file.write('FLASK_ENV=development\n'
                   'DATABASE_CONNECTION_STRING=sqlite:///static/DB/flask_app.db\n')
        file.close()
        print('Env file created.')

    load_dotenv()


def init_db(app):
    if not os.path.isdir('static/DB'):
        os.makedirs('static/DB')
        print('DB folder created.')

    db.app = app
    db.init_app(app)
    db.create_all()

    if not os.path.isdir('static/DATA'):
        os.makedirs('static/DATA')
        print('DATA folder created.')


def init_loggers():
    # -- LOGGERS -- #
    logger = logging.getLogger('logger')
    error_logger = logging.getLogger('error_logger')

    logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.DEBUG)

    if not os.path.isdir('Logs'):
        os.makedirs('Logs')
        print('Logs folder created.')

    fh = logging.FileHandler('Logs/info.log')
    fher = logging.FileHandler('Logs/error.log')
    ch = logging.StreamHandler()

    fh.setLevel(logging.INFO)
    fher.setLevel(logging.DEBUG)
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    fher.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    error_logger.addHandler(fher)
    error_logger.addHandler(ch)


def init_debug():
    try:
        print('Debug data initialization...')
        print(UserDAO.delete_all(UserDAO.get_all()))
        # Add users
        UserDAO.create('admin@gmail.com', 'admin1')
        UserDAO.create('user@gmail.com', 'user1')
        print('New data created.')

        print('Initialization completed.')
    except Exception as e:
        db.session.rollback()
        print('Error: ' + e.__str__())
