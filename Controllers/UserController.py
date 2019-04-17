import os
import shlex
import logging
import datetime
import subprocess

from DAL import data_path
from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO

from Controllers import user_controller

from werkzeug.utils import secure_filename

from Utilities.Authentication import Authentication
from Utilities.CustomExceptions import UserException, DatabaseException

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
        except UserException as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))
        except Exception as e:
            session.pop('auth_token', None)
            logging.getLogger('error_logger').exception(e)
            return redirect(url_for('home_controller.index', error='Something went wrong.'))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))


@user_controller.route('/prime-zombies', methods=['POST'])
def release_zombies():
    logging.getLogger('logger').info('Processing started')
    try:
        user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        user = UserDAO.get(user_id)
        data = subprocess.run(shlex.split('mpiexec -n ' +
                                          request.form['threads'] +
                                          #' -f MPI/hostfile' +
                                          ' python MPI/StartScript.py ' +
                                          os.path.join(user.home_catalog, 'INPUT') + ' ' +
                                          '1920 1080 20 ' +
                                          os.path.join(user.home_catalog, 'INPUT/test.zip')),
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

        return jsonify(output)
    else:
        return jsonify(data.stderr.decode('utf-8').split('\n'))


@user_controller.route('add_file', methods=['POST'])
def add_file():
    file_front = request.files['filePath']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        file_back = FileDAO.create(file_front.filename, user)
        file_front.save(data_path + file_back.input_path + secure_filename(file_front.filename))
        return redirect(url_for('user_controller.index'))
    except DatabaseException as e:
        session.pop('auth_token', None)
        return redirect(url_for('home_controller.index', error=e))
    except UserException as e:
        return redirect(url_for('user_controller.index', error=e))
    except Exception as e:
        logging.getLogger('error_logger').exception(e)
        return redirect(url_for('user_controller.index', error='File cannot be uploaded.'))


@user_controller.route('get_files', methods=['GET'])
def get_files():
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
    except UserException as e:
        session.pop('auth_token', None)
        return redirect(url_for('home_controller.index', error=e))

    data = []
    for elem in user.files:
        data.append(elem.as_dict())
    return jsonify(data)


@user_controller.route('queue_file', methods=['POST'])
def queue_file():
    raise NotImplementedError


@user_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index'))
