from flask import Flask
from app.config.extensions import compress, cors, bcrypt, migrate, db, jwt, admin
from app.routes.auth import auth_bp
from app.routes.alumni import alumni_bp
from app.routes.house_master import house_master_bp
from app.config.config import EnvConfig
from app.utils.mini import check_empty_roles
from flask_admin.contrib.sqla import ModelView
from app.database.models import Users, Role, House, Course
from app.database.schemes import RoleView, UserView, HouseView



def alumni_app():
    config = EnvConfig()
    app = Flask(__name__)

    app.config.from_object(config)

    compress.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)

    admin.add_view(UserView(Users, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(HouseView(House, db.session))
    admin.add_view(ModelView(Course, db.session))
    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(alumni_bp, url_prefix='/alumni')
    app.register_blueprint(house_master_bp, url_prefix='/master')

    with app.app_context():
        check_empty_roles()
        
        
    
    return app