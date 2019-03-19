import logging

from flask import Blueprint, render_template, session, redirect, url_for, current_app

from BLL.UserManager import UserManager

logger = logging.getLogger('logger')
error_logger = logging.getLogger('error_logger')

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/')
def index():
    if 'auth_token' in session:
        login = UserManager.get_user(current_app.config['SECRET_KEY'], session['auth_token']).login
        return render_template('userPanel.html', user=login)
    return render_template('error.html', error='You have to log in first.')


@user_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index'))
