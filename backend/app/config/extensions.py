from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_admin import Admin


bcrypt = Bcrypt()
compress = Compress()
cors = CORS()
migrate = Migrate() 
db = SQLAlchemy()
jwt = JWTManager()
admin = Admin(name='Alumni Connect', template_mode='bootstrap4')