import datetime
import logging
import traceback

from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for

from BLL.UserManager import UserManager
from Utilities.Authentication import Authentication
from Utilities.Counter import Counter
from Utilities.Format import Format
from Utilities.PropertiesReader import PropertiesReader

logger = logging.getLogger('logger')
error_logger = logging.getLogger('error_logger')

home_controller = Blueprint('home_controller', __name__)
data = PropertiesReader('Controllers/static/dictionary/feedback_index.properties')

likes_counter = Counter(990)


@home_controller.route('/')
def index():
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    number = Format.human_format(likes_counter.get())
    complete_data = data.read('key1')
    current_year = datetime.datetime.now().year.__str__()
    return render_template('index.html', date=current_date, likes=number, question_data=complete_data,
                           year=current_year)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    likes_counter.add(1)
    logger.info('Like added.')
    number = Format.human_format(likes_counter.get())
    return jsonify(number)


@home_controller.route('/account', methods=['POST', 'GET'])
def login_process():
    try:
        if request.method == 'POST':
            login = request.form['email']
            password = request.form['password']
            user = UserManager.check_user(login, password)
            logger.info("User " + user.login + " signed in.")

            token = Authentication.generate_auth_token(user.login, user.hashed_password)
            session['auth_token'] = token
            session['username'] = user.login
            return render_template('userPanel.html', user=user.login)
        else:
            if 'username' in session:
                return render_template('userPanel.html', user=session['username'])
            else:
                return render_template('error.html', error='You have to sign in first.')

    except Exception as e:
        tb = traceback.format_exc()
        error_logger.error(tb.__str__())
        logger.error(e.__str__())
        return render_template('error.html', error='Incorrect login data.')


@home_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    session.pop('username', None)
    return redirect(url_for('home_controller.index'))
