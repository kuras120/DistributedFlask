import os
import logging
from flask import Flask

from Project.Server.ORM import db
from Project.Server.Tasks import make_celery
from Project.Config import init_loggers, init_debug

from Project.Server.Controllers.HomeController import home_controller
from Project.Server.Controllers.UserController import user_controller


def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder='Client/templates',
        static_folder='Client/static'
    )

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    if not app_settings:
        app_settings = 'Project.Config.DevelopmentGlobalConfig'
    app.config.from_object(app_settings)

    celery = make_celery(app)
    logging.getLogger('logger').info('Celery initialized.')

    init_loggers()
    logging.getLogger('logger').info('Loggers initialized.')

    db.app = app
    db.init_app(app)
    db.create_all()
    logging.getLogger('logger').info('Db initialized.')

    if os.getenv('FLASK_ENV') == 'development':
        init_debug()
        logging.getLogger('logger').info('Debug mode on')

    # register blueprints
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')

    # shell context for flask cli
    app.shell_context_processor({'app': app})

    return app, celery
