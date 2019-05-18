import datetime

from flask import Blueprint

from multiprocessing import Value

from Project.Server.DAL.UserDAO import UserDAO

from Project.Server.Utilities.Format import Format
from Project.Server.Utilities.Authentication import Authentication

from flask import render_template, jsonify, request, session, redirect, url_for, current_app

likes_counter = Value('i', 1200)
home_controller = Blueprint('home_controller', __name__)


@home_controller.route('/', defaults={'error': None})
@home_controller.route('/<error>')
def index(error):
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    likes = Format.human_format(likes_counter.value)
    current_year = datetime.datetime.now().year.__str__()
    login = None
    if 'auth_token' in session:
        error = None
        try:
            login = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'],
                                                                 session['auth_token'])).login.split('@')[0]
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))

    return render_template('index.html', date=current_date, year=current_year, user=login, likes=likes, error=error)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    with likes_counter.get_lock():
        likes_counter.value += 1
    number = Format.human_format(likes_counter.value)
    return jsonify(number)


@home_controller.route('/login_process', methods=['POST'])
def login_process():
    try:
        user = UserDAO.read(request.form['email'], request.form['password'])
        session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('home_controller.index', error=e))


@home_controller.route('/register_process', methods=['POST'])
def register_process():
    if request.form['passwordRegister'] == request.form['conf_password']:
        try:
            user = UserDAO.create(request.form['emailRegister'], request.form['passwordRegister'])
            session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
            return redirect(url_for('user_controller.index'))
        except Exception as e:
            return redirect(url_for('home_controller.index', error=e))
    else:
        return redirect(url_for('home_controller.index', error='Passwords don\'t match.'))


@home_controller.route('/logout', defaults={'error': None})
@home_controller.route('/logout/<error>')
def logout(error):
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index', error=error))
