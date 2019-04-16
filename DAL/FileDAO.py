import os
import logging

from ORM import db
from ORM.File import File
from ORM.History import History, TypeH

from Utilities.CustomExceptions import UserException, DatabaseException


class FileDAO:
    @staticmethod
    def create(file_name, description, user):
        try:
            if not db.session.query(File).filter(File.name == file_name, File.user_id == user.id).first():
                new_data = File(name=file_name, description=description, login=user.login)
                user.data.append(new_data)
                h_log = History(type_h=TypeH.Info, description='File ' + new_data.name + ' added')
                user.history.append(h_log)
                db.session.merge(user)
                db.session.commit()
                if not os.path.isdir(os.path.dirname('static/DATA/' + new_data.file_path)):
                    os.makedirs(os.path.dirname('static/DATA/' + new_data.file_path))
                open('static/DATA/' + new_data.file_path, 'w+').close()
                return new_data
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'File with this name already exists.'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read(file_name, user):
        try:
            data = db.session.query(File).filter(File.name == file_name, File.user_id == user.id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
        if data:
            return data
        else:
            logging.getLogger('logger').warning('File not found.')
            raise UserException()

    @staticmethod
    def update(data, user, info):
        if data and user:
            try:
                db.session.merge(data)
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
    def delete(data):
        if data:
            try:
                db.session.delete(data)
                db.session.commit()
                if os.path.isfile('static/DATA/' + data.file_path):
                    os.remove('static/DATA/' + data.file_path)
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Delete data error. Data not found.')
            raise UserException('Data doesn\'t exists.')

    @staticmethod
    def delete_all(data):
        try:
            for dt in data:
                db.session.delete(dt)
            db.session.commit()
            for dt in data:
                if os.path.isfile('static/DATA/' + dt.file_path):
                    os.remove('static/DATA/' + dt.file_path)
            return 'All data dropped.'
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
