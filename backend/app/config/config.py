from datetime import timedelta
import os

class EnvConfig:
    REDIS_URL = os.environ['REDIS_URL']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    FLASK_ADMIN_SWATCH = 'darkly'
    SECURITY_PASSWORD_SALT=os.environ['SECURITY_PASSWORD_SALT']
    SECURITY_EMAIL_VALIDATOR_ARGS={"check_deliverability": False}
    


    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        if self.CACHE_REDIS_URL is None:
            self.CACHE_REDIS_URL = self.REDIS_URL

    SQLALCHEMY_ENGINE_OPTIONS:dict[str, bool|int] = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20
    }

   


class TestConfig:
    TESTING: bool =True
    SQLALCHEMY_DATABASE_URI: str 
    