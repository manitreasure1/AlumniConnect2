from flask import request, jsonify, make_response
from app.database.schemes import RegisterUser, LoginUser, UpdateUser
from .user_service import UserService
from werkzeug.exceptions import Forbidden, NotFound
from flask_jwt_extended import create_access_token, create_refresh_token
from app.config.extensions import bcrypt, db, jwt
from app.database.models import Users
from flask_jwt_extended import get_jwt, create_refresh_token, get_jwt_identity
from app.config.config import EnvConfig
from app.utils.redis_ import jwt_redis_block_list
import logging
from typing import Any


user_service = UserService()
config = EnvConfig()


@jwt.user_lookup_loader
def users_lookup_callback(jwt_header, jwt_data: dict[Any, Any]):
    try:
        identity = jwt_data['sub']
        if not(isinstance(identity, str)):
            logging.error('this is not of obj str')
            return None
        try:
            user_id_uuid = identity
        except ValueError:
            logging.error('not valid uuid')
            return None

        return Users.get_user_by_id(user_id_uuid)
    except Exception as e:
        logging.exception(e)
        return None


@jwt.token_in_blocklist_loader
def check_revoked_token(jwt_header, jwt_data: dict[Any, Any]):
    user_id = jwt_data['jti']
    token_in_redis = jwt_redis_block_list.get(str(user_id))
    print(f"Checking Token {user_id}: {token_in_redis}") 
    return token_in_redis is not None    



class AuthService:
    def sign_up(self):
        user_data = request.get_json()
        validate_reqest_data = RegisterUser(**user_data)

        existing_user = user_service.existing_user(validate_reqest_data.email)

        if existing_user:
            raise Forbidden("User Already Exist", )
        hash_password = bcrypt.generate_password_hash(validate_reqest_data.password).decode('utf-8')
        _new_user = Users(
            firstname=validate_reqest_data.firstname, # type: ignore
            lastname=validate_reqest_data.lastname, # type: ignore
            email=validate_reqest_data.email, # type: ignore
            username=validate_reqest_data.email.split('@')[0], # type: ignore
            password_hash=hash_password, # type: ignore
            role_id=user_service.get_user_role('student') # type: ignore
        )
        db.session.add(_new_user)
        db.session.commit()
        db.session.refresh(_new_user)
        response = make_response(jsonify({
            "msg":"Account Created Successfully",
            "category":"success",
            }), 201)
        return response
    

    def login(self):
        user_data = request.get_json()
        validate_reqest_data = LoginUser(**user_data)

        userdb = user_service.get_user_by_email(validate_reqest_data.email)

        if userdb is None:
            raise Forbidden(description='Invalid email or password')
        validate_password = bcrypt.check_password_hash(userdb.password_hash, validate_reqest_data.password) 
        
        if not validate_password:
            raise Forbidden(description='Invalid email or password')
        payload = userdb.user_id
        access_token = create_access_token(payload, fresh=True)
        refresh_token = create_refresh_token(payload)
        response = make_response(jsonify({
            "msg":"Login Successfully",
            "category":"success",
            "access_token": access_token,
            "refresh_token": refresh_token
            }), 200)
        return response
    


    def update_(self):
        update_user = request.get_json()
        
        user_id = get_jwt_identity()
        print(user_id)
        user_db = user_service.get_user_by_id(user_id)
        if not user_db:
            raise NotFound("User Not Found")
        
        user_instance = UpdateUser(**update_user)  
        user_data = user_instance.model_dump(exclude_unset=True) 
        for key, value in user_data.items():
            setattr(user_db, key, value)
        db.session.add(user_db)
        db.session.commit()
        db.session.refresh(user_db)
        return make_response("", 204)
    
    def refresh(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)
    

    def logout(self):
        jti = get_jwt()['jti']
        jwt_redis_block_list.set(jti, b'true', ex=config.JWT_ACCESS_TOKEN_EXPIRES)
        print("Stored tokens in Redis:", jwt_redis_block_list.keys("*"))
        response = make_response(jsonify({"msg":"User Logout Successfully", "category":"success"}), 200)
        return response


