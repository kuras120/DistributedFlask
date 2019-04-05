import os
import logging
import secrets

from flask import Flask

from Config import init_loggers, init_debug, init_db, bind_blueprints

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/DB/flask_app.db'

init_loggers()
logging.getLogger('logger').info('Loggers initialized.')

bind_blueprints(app)
logging.getLogger('logger').info('Blueprints created.')

init_db(app)
logging.getLogger('logger').info('Db initialized.')

if os.environ.get('FLASK_ENV') == 'development':
    init_debug()
    logging.getLogger('logger').info('Debug mode on')

if __name__ == '__main__':
    app.run()
