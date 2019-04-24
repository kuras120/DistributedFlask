import os
import logging

from ORM import db
from ORM.File import File
from ORM.History import History, TypeH

from werkzeug.utils import secure_filename
from Utilities.CustomExceptions import UserException, DatabaseException


class FileDAO:
    @staticmethod
    def create(file, user):
        try:
            secure_name = secure_filename(file.filename)
            if not db.session.query(File).filter(File.name == secure_name, File.user_id == user.id).first():
                new_data = File(name=secure_name)
                user.files.append(new_data)
                h_log = History(type_h=TypeH.Info, description='File ' + new_data.name + ' added')
                user.history.append(h_log)
                db.session.merge(user)
                db.session.commit()
                path = os.path.join('static/DATA/' + user.home_catalog, new_data.name)
                if not os.path.isfile(path):
                    file.save(path)
                return new_data
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'File with this name already exists.'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read(name, user_id):
        try:
            file = db.session.query(File).filter(File.name == name, File.user_id == user_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
        if file:
            return file
        else:
            logging.getLogger('logger').warning('File not found.')
            raise UserException()

    @staticmethod
    def update(file, user, info=None):
        if file and user:
            try:
                db.session.merge(file)
                if info:
                    h_log = History(type_h=TypeH.Info, description=info)
                    user.history.append(h_log)
                    db.session.merge(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Update data error. Data not found.')
            raise UserException('Data doesn\'t exists.')

    @staticmethod
    def delete(files, home_catalog):
        try:
            for dt in files:
                db.session.delete(dt)
            db.session.commit()
            for dt in files:
                path = os.path.join('static/DATA/' + home_catalog, dt.name)
                if os.path.isfile(path):
                    os.remove(path)
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get(data_id):
        try:
            return db.session.query(File).filter(File.id == data_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get_all(user_id):
        try:
            return db.session.query(File).filter(File.user_id == user_id).all()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
