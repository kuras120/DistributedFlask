import datetime
import logging
import traceback

from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, current_app

from BLL.UserManager import UserManager
from Utilities.Authentication import Authentication
from Utilities.Counter import Counter
from Utilities.Format import Format
from Utilities.PropertiesReader import PropertiesReader

logger = logging.getLogger('logger')
error_logger = logging.getLogger('error_logger')

home_controller = Blueprint('home_controller', __name__)
data = PropertiesReader('static/dictionary/feedback_index.properties')

likes_counter = Counter(990)


@home_controller.route('/')
def index():
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    number = Format.human_format(likes_counter.get())
    complete_data = data.read('key1')
    current_year = datetime.datetime.now().year.__str__()
    login = None
    if 'auth_token' in session:
        login = UserManager.get_user(current_app.config['SECRET_KEY'], session['auth_token']).login
    return render_template('index.html', date=current_date, likes=number, question_data=complete_data,
                           year=current_year, user=login)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    likes_counter.add(1)
    logger.info('Like added.')
    number = Format.human_format(likes_counter.get())
    return jsonify(number)


@home_controller.route('/account', methods=['POST'])
def login_process():
    try:
        user = UserManager.check_user(request.form['email'], request.form['password'])
        logger.info("User " + user.login + " signed in.")
        session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        tb = traceback.format_exc()
        error_logger.error(tb.__str__())
        logger.error(e.__str__())
        return render_template('error.html', error='Incorrect login data.')

