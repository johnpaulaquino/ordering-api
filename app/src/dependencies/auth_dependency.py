from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from app.src.database.repositories.customer_repositories import CustomerRepository
from app.src.security.auth_security import AuthSecurity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/auth/token')
class AuthDependency:


     @staticmethod
     async def get_current_user(token: str = Depends(oauth2_scheme)):
          try:
               payload = AuthSecurity.decode_jwt_token(token)

               data = await CustomerRepository.get_customer_by_id(payload.get('user_id'))

               if not data:
                    raise HTTPException(
                            status_code= status.HTTP_404_NOT_FOUND,
                            detail={'status':'fail', 'message':'User not found'},
                            headers={'WWW-Authenticate':'Bearer'})
               #otherwise return the customer data
               del data.password
               return data




          except Exception as e:
               raise e
