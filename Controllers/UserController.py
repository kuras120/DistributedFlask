import shlex
import logging
import datetime
import subprocess


from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO

from Controllers import user_controller

from werkzeug.utils import secure_filename

from Utilities.Authentication import Authentication


from flask import render_template, session, redirect, url_for, current_app, jsonify, request


@user_controller.route('/', defaults={'error': None})
@user_controller.route('/<error>')
def index(error):
    if 'auth_token' in session:
        try:
            user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
            login = UserDAO.get(user_id).login.split('@')[0]
            current_year = datetime.datetime.now().year.__str__()
            return render_template('userPanel.html', user=login, year=current_year, error=error)
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))


@user_controller.route('/prime-zombies', methods=['POST'])
def release_zombies():
    logging.getLogger('logger').info('Processing started')
    try:
        data = subprocess.run(shlex.split('mpiexec -n ' +
                                          request.form['threads'] +
                                          #' -f MPI/hostfile' +
                                          ' python MPI/StartScript.py ' +
                                          request.form['numbers'] + ' ' +
                                          request.form['parts']),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        logging.getLogger('error_logger').exception(e)
        return jsonify(e)

    if not data.stderr:
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
    else:
        return jsonify(data.stderr.decode('utf-8').split('\n'))


@user_controller.route('add_file', methods=['POST'])
def add_file():
    name = request.form['name']
    description = request.form['description']
    file_front = request.files['file_path']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        file_back = FileDAO.create(name, description, user)
    except Exception as e:
        session.pop('auth_token', None)
        return redirect(url_for('home_controller.index', error=e))

    try:
        file_front.save(file_back.input_path, secure_filename(name))
    except Exception as e:
        logging.getLogger('error_logger').exception(e)
        return redirect(url_for('user_controller.index', error='File cannot be uploaded. Try later.'))


@user_controller.route('get_files', methods=['GET'])
def get_files():
    user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
    return jsonify(user.files)


@user_controller.route('queue_file', methods=['POST'])
def queue_file():
    raise NotImplementedError


@user_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index'))
