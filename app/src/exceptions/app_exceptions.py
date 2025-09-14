class AppException(Exception):
     def __init__(self, status_code=500,
                  message="Internal Server Error, please contact the developer.",
                  message_status='error',
                  headers : dict = None):
          self.message = message
          self.status_code = status_code
          self.message_status = message_status
          self.headers = headers
          super().__init__(status_code, message, message_status,headers)


class DatabaseDataNotFoundException(AppException):
     """When try to retrieve personal information in database, but not found."""
     pass


class DatabaseDuplicateEntryException(AppException):
     """When try to insert in data in database, but it is already in database."""
     pass


class JWTErrorException(AppException):
     """When credential from token is not validated or when token is expired"""
     pass
