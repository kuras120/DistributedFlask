import os
import secrets
import logging

from flask import Flask

from ORM.DbConfig import init_db
from Config import Config

from ORM.DbConfig import db_session

from HomeController import home_controller
from UserController import user_controller


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    # Bind controllers
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')
    logging.getLogger('logger').info('Blueprints created.')
    Config.init_loggers()
    logging.getLogger('logger').info('Loggers initialized.')
    init_db()
    logging.getLogger('logger').info('Db initialized.')

    if os.environ.get('FLASK_ENV') == 'development':
        Config.init_debug()
        logging.getLogger('logger').info('Debug mode on')

    app.run()


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
