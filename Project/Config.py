import os
import secrets
import logging

from Project.Server.DAL.UserDAO import UserDAO


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Server/flask_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(16)
    REDIS_URL = 'redis://127.0.0.1:6379/0'
    FLASK_ENV = 'production'
    WTF_CSRF_ENABLED = True
    QUEUES = ['default']


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    FLASK_ENV = 'development'
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    FLASK_ENV = 'development'
    WTF_CSRF_ENABLED = False
    TESTING = True


def init_loggers():
    # -- LOGGERS -- #
    logger = logging.getLogger('logger')
    error_logger = logging.getLogger('error_logger')

    logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.DEBUG)

    if not os.path.isdir('Project/Logs'):
        os.makedirs('Project/Logs')
        print('Logs folder created.')

    fh = logging.FileHandler('Project/Logs/info.log')
    fher = logging.FileHandler('Project/Logs/error.log')
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
        UserDAO.delete(UserDAO.get_all())
        # Add users
        UserDAO.create('admin@gmail.com', 'admin1')
        UserDAO.create('user@gmail.com', 'user1')
        print('New data created.')

        print('Initialization completed.')
    except Exception as e:
        print('Error: ' + e.__str__())
