from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, jwt
from passlib.context import CryptContext

from app.config.settings import Settings

settings = Settings()


class AuthSecurity:
     __bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

     @classmethod
     def hash_password(cls, plain_password: str):
          return cls.__bcrypt_context.hash(plain_password)

     @classmethod
     def verify_hashed_password(cls, plain_password: str, hashed_password: str):
          return cls.__bcrypt_context.verify(plain_password, hashed_password)

     @classmethod
     def generate_access_token(cls, data_: dict, expiration: int = 0):
          to_encode = data_.copy()
          expires = datetime.now(timezone.utc) + timedelta(minutes=5)
          if expiration > 0:
               expires = datetime.now(timezone.utc) + timedelta(days=expiration)

          to_encode.update({'exp': expires})

          access_token = jwt.encode(to_encode, key=settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
          return access_token

     @classmethod
     def generate_refresh_access_token(cls, data_: dict, expiration: int = 0):
          to_encode = data_.copy()
          expires = datetime.now(timezone.utc) + timedelta(days=3)
          if expiration > 0:
               expires = datetime.now(timezone.utc) + timedelta(days=expiration)

          to_encode.update({'exp': expires})

          access_token = jwt.encode(to_encode, key=settings.JWT_KEY, algorithm=settings.JWT_ALGORITHMs)
          return access_token

     @staticmethod
     def decode_jwt_token(token: str):
          try:
               err_message = HTTPException(
                       status_code=status.HTTP_401_UNAUTHORIZED,
                       detail={'status': 'failed', 'message': 'Could not validate credentials'},
                       headers={"WWW-Authenticate": 'Bearer'})
               if not token:
                    raise err_message

               payload = jwt.decode(token, key=settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])

               if not payload:
                    raise err_message

               return payload

          except ExpiredSignatureError as e:
               raise e