from flask import Blueprint
import logging 
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("authentication",__name__)
auth_service = AuthService()




@auth_bp.route("/register/", methods=['POST'])
def signup():
    try:
        register = auth_service.sign_up()
        return register
    except Exception as e:
        logging.exception(e)
        raise e
   
    
@auth_bp.route("/login/", methods=['POST'])
def login():
    try:
        sign_in = auth_service.login()
        return sign_in
    except Exception as e:
        logging.exception(e)
        raise e


@auth_bp.route("/refresh")
@jwt_required()
def refresh():
    try:
        refresh_token = auth_service.refresh()
        return refresh_token
    except Exception as e:
        raise e



@auth_bp.route("/update/", methods=['PUT'])
@jwt_required()
def update_user():
    try:
        new_data = auth_service.update_()
        return new_data
    except Exception as e:
        logging.exception(e)
        raise e


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    try:
        logout_user = auth_service.logout()
        return logout_user
    except Exception as e:
        logging.exception(e)
        raise e