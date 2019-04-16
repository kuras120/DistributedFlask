import os
import shutil
import logging

from ORM import db
from ORM.File import File
from ORM.History import History, TypeH

from DAL import data_path

from Utilities.CustomExceptions import UserException, DatabaseException


class FileDAO:
    @staticmethod
    def create(file_name, user, description=None):
        try:
            if not db.session.query(File).filter(File.name == file_name, File.user_id == user.id).first():
                new_data = File(name=file_name, user_catalog=user.home_catalog, description=description)
                user.files.append(new_data)
                h_log = History(type_h=TypeH.Info, description='File ' + new_data.name + ' added')
                user.history.append(h_log)
                db.session.merge(user)
                db.session.commit()
                return new_data
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'File with this name already exists.'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read(file_name, user_id):
        try:
            data = db.session.query(File).filter(File.name == file_name, File.user_id == user_id).first()
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
                if os.path.isfile(data_path + data.input_path + data.name):
                    os.remove(data_path + data.input_path + data.name)
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Delete data error. Data not found.')
            raise UserException('Data doesn\'t exists.')

    @staticmethod
    def delete_all(user):
        try:
            for data in user.files:
                db.session.delete(data)
            db.session.commit()
            if os.path.isdir(data_path + user.home_catalog):
                shutil.rmtree(data_path + user.home_catalog)
            os.makedirs(data_path + user.home_catalog)
            os.makedirs(data_path + user.home_catalog + '/INPUT')
            os.makedirs(data_path + user.home_catalog + '/OUTPUT')
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
