import shlex
import logging
import datetime
import subprocess

from flask import render_template, session, redirect, url_for, current_app, jsonify, request

from Utilities.Authentication import Authentication
from Controllers import user_controller
from DAL.UserManager import UserManager


@user_controller.route('/')
def index():
    if 'auth_token' in session:
        try:
            user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
            login = UserManager.get_user(user_id).login
            current_year = datetime.datetime.now().year.__str__()
            return render_template('userPanel.html', user=login, year=current_year)
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))


@user_controller.route('/prime-zombies', methods=['POST'])
def release_zombies():
    logging.getLogger('logger').info('Processing started')
    data = subprocess.run(shlex.split('mpiexec -n ' +
                                      request.form['threads'] +
                                      ' python MPI/StartScript.py ' +
                                      request.form['numbers'] + ' ' +
                                      request.form['parts']),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ''
    for line in data.stdout.decode('utf-8').split('\n'):
        if 'output' in line:
            output = line
        else:
            if line:
                logging.getLogger('logger').info(line.strip())

    logging.getLogger('logger').info('Processing completed')
    logging.getLogger('logger').info(output)

    return jsonify(output.split(':')[1].strip())


@user_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index'))
