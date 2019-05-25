import os
import ast
import json
import redis
import logging
import datetime
import urllib.parse

from flask import Blueprint

from rq import Queue, Connection

from werkzeug.utils import secure_filename

from Project.Server.DAL.UserDAO import UserDAO
from Project.Server.DAL.FileDAO import FileDAO

from Project.Server.Tasks.MpiTasks import raytracing_task

from Project.Server.Utilities.Authentication import Authentication

from flask import render_template, session, redirect, url_for, current_app, jsonify, request

user_controller = Blueprint('user_controller', __name__)


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


@user_controller.route('/queue_task', methods=['GET', 'POST'])
def queue_task():
    try:
        user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        user = UserDAO.get(user_id)
        directory = os.path.join('Project/Server/DATA', user.home_catalog)
        task_name = secure_filename(request.form['taskName'])
        resolution = ast.literal_eval(request.form['resolutionSelect'])
        file = request.form['fileSelect']

        if task_name + '.mp4' not in os.listdir(directory):
            with Connection(redis.from_url(current_app.config['REDIS_URL'])):
                q = Queue(default_timeout=600)
                task = q.enqueue(raytracing_task, directory, resolution, file, task_name)
            response_object = {
                'status': 'success',
                'data': {
                    'task_id': task.get_id()
                }
            }
            return jsonify(response_object), 202
        else:
            logging.getLogger('logger').warning('Filename already exists.')
            return jsonify('Filename already exists.'), 500

    except Exception as e:
        logging.getLogger('error_logger').exception(e)
        return redirect(url_for('user_controller.index', error='Unexpected error occurred. Please, contact support'))


@user_controller.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)


@user_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))
