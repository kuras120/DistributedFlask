import os
import json
import shlex
import logging
import datetime
import subprocess
import urllib.parse

from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO

from Controllers import user_controller

from Utilities.Authentication import Authentication

from flask import render_template, session, redirect, url_for, current_app, jsonify, request


@user_controller.route('/', defaults={'error': None})
@user_controller.route('/<error>')
def index(error):
    user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
    try:
        login = user.login.split('@')[0]
        files = FileDAO.get_all(user.id)
        current_year = datetime.datetime.now().year.__str__()
        return render_template('userPanel.html', user=login, files=files, year=current_year, error=error)
    except Exception as e:
        return redirect(url_for('home_controller.logout', error=e))


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
                                          'static/DATA/' +
                                          os.path.join(user.home_catalog, 'INPUT') + ' ' +
                                          '1920 1080 20 ' + 'test.zip'),
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


@user_controller.route('/add_file', methods=['POST'])
def add_file():
    file = request.files['filePath']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        FileDAO.create(file, user)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


@user_controller.route('/delete_files', methods=['POST'])
def delete_files():
    try:
        data = json.loads(urllib.parse.unquote(request.get_data('files').decode('utf-8')))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        data_entities = []
        for name in data:
            data_entities.append(FileDAO.read(name, user.id))
        FileDAO.delete(data_entities, user.home_catalog)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


@user_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))
