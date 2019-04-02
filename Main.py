import secrets
import logging

from flask import Flask

from Config import init_config
from ORM.DbConfig import db_session

from HomeController import home_controller
from UserController import user_controller


if __name__ == '__main__':
    app = Flask(__name__)
    # Main Config
    init_config()
    # Secret key
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    # Bind controllers
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')
    logging.getLogger('logger').info('Blueprints created.')
    app.run()


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
