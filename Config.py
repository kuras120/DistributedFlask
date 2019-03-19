import logging
import secrets

from flask import Flask

from HomeController import home_controller
from UserController import user_controller
from ORM.DbConfig import init_db, db_session


# -- LOGGERS -- #
main_logger = logging.getLogger('logger')
error_logger = logging.getLogger('error_logger')

main_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('Logs/info.log')
fh.setLevel(logging.INFO)

fher = logging.FileHandler('Logs/error.log')
fher.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

fher.setFormatter(formatter)
ch.setFormatter(formatter)

main_logger.addHandler(fh)

error_logger.addHandler(fher)
error_logger.addHandler(ch)

# -- APP -- #
app = Flask(__name__)
# Debug mode
app.config['DEBUG'] = True
# Secret key
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
# Bind controllers
app.register_blueprint(home_controller, url_prefix='/')
app.register_blueprint(user_controller, url_prefix='/account')
main_logger.info("Blueprints created.")

# Init database
init_db()
main_logger.info("Db initialized.")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# TODO logger tylko do najwazniejszych operacji. Zamiast niego historia do bazy danych.
