
class UserException(Exception):
    def __init__(self, message='Wrong username or password.'):
        super(Exception, self).__init__(message)


class DatabaseException(Exception):
    def __init__(self, message='Database connection error. Try log in later.'):
        super(Exception, self).__init__(message)
