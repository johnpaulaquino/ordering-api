import requests
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette.responses import JSONResponse, RedirectResponse

from app.config.settings import Settings
from app.logs import Logger
from app.src.database.models.customers import Customer
from app.src.database.repositories.customer_repositories import CustomerRepository
from app.src.exceptions.app_exceptions import AppException, DatabaseDataNotFoundException, JWTErrorException
from app.src.security.auth_security import AuthSecurity

auth_router = APIRouter(
        tags=['Authentication'],
        prefix='/api/v1/auth',
)

settings = Settings()


@auth_router.get("/google")
async def login_via_google():
     """

     :return:
     """
     google_auth_url = (
             "https://accounts.google.com/o/oauth2/v2/auth"
             f"?client_id={settings.GOOGLE_CLIENT_ID}"
             f"&redirect_uri=http://127.0.0.1:5500/test_home.html"
             "&response_type=code"
             "&scope=openid%20email%20profile"
     )
     return RedirectResponse(url=google_auth_url)


@auth_router.get('/google/callback')
async def oauth_callback(code: str):
     """
     :param code:
     :return:
     """
     try:
          token_url = "https://oauth2.googleapis.com/token"
          token_data = {
                  "code"         : code,
                  "client_id"    : settings.GOOGLE_CLIENT_ID,
                  "client_secret": settings.GOOGLE_CLIENT_SECRET,
                  "redirect_uri" : 'http://127.0.0.1:5500/test_home.html',
                  "grant_type"   : "authorization_code",
          }

          token_response = requests.post(token_url, data=token_data).json()
          if "id_token" not in token_response:
               raise JWTErrorException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       message_status='fail',
                       message='Invalid request',
                       headers={'WWW-Authenticate': 'Bearer'})

          # decode token that came from Google
          try:
              user_info = jwt.get_unverified_claims(token_response["id_token"])
          except Exception as e:
               raise e

          user_email = user_info['email']
          username = user_info['name']
          given_name = user_info['given_name']
          family_name = user_info['family_name']

          user_data = {'user_email': user_email}

          data = await CustomerRepository.get_customer_by_email(user_email)

          new_user = Customer(username=username, email=user_email)

          if not data:
               #insert in database
               await CustomerRepository.create_user(new_user)

               #prepare the user id to encode in access_token
               to_encode = {'user_id': new_user.id}
               # generate access token
               generated_access_token = AuthSecurity.generate_access_token(to_encode)
               #prepare the user id to encode in refresh_access_token
               data_refresh_token = {'user_id': data.id, 'user_email': data.email}
               generated_refresh_access_token = AuthSecurity.generate_refresh_access_token(data_refresh_token)
               Logger.info(msg=f'Created Account')
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status'              : 'ok', 'message': 'Successfully created account',
                                'action'              : 'signup',
                                'access_token'        : generated_access_token,
                                'refresh_access_token': generated_refresh_access_token,
                                'access_type'         : 'bearer'
                                })
          # if not exist which is signup
          to_encode = {'user_id': data.id}
          generated_access_token = AuthSecurity.generate_access_token(to_encode)
          data_refresh_token = {'user_id': data.id, 'user_email': data.email}

          return JSONResponse(
                  status_code=status.HTTP_200_OK,
                  content={'status'              : 'ok',
                           'action'              : 'login',
                           'access_token'        : generated_access_token,
                           'refresh_access_token': data_refresh_token,
                           'access_type'         : 'bearer'}, )

     except Exception as e:
          raise e


@auth_router.post('/token')
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
     try:
          data = await CustomerRepository.get_customer_by_email(form_data.username)
          if not data:
               raise DatabaseDataNotFoundException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       message_status='fail',
                       message='User not found',
                       headers={'WWW-Authenticate': 'Bearer'})

          if not AuthSecurity.verify_hashed_password(form_data.password, data.password):
               raise DatabaseDataNotFoundException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       message_status='fail',
                       message='Incorrect password',
                       headers={'WWW-Authenticate': 'Bearer'})
          to_encode = {'user_id': data.id, 'user_name': data.username}
          access_token = AuthSecurity.generate_access_token(to_encode)
          Logger.info(msg=f'{data.id} logged in')
          return JSONResponse(
                  status_code=status.HTTP_200_OK,
                  content={'access_token': access_token, 'access_type': 'Bearer'},
          )
     except Exception as e:
          if not isinstance(e, AppException):
               Logger.critical(msg=f"{e}")
          raise e
