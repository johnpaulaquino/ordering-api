from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
     DB_URL: str

     JWT_KEY: str
     JWT_ALGORITHM: str
     JWT_EXPIRATION_REFRESH_TOKEN: int


     #GOOGLE
     GOOGLE_CLIENT_ID : str
     GOOGLE_CLIENT_SECRET : str
     REDIRECT_URI : str
