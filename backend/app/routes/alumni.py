from flask import Blueprint
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required


alumni_bp = Blueprint('student', __name__)
user_services = UserService()


@alumni_bp.route("/me/dashboard")
@jwt_required()
def my_dashboard():
    try:
        user_data = user_services.alumni_dashboard()
        return user_data
    except Exception as e:
        raise e

@alumni_bp.route("/house", methods=["POST"])
@jwt_required()
def reister_house():
    try:
        house_data = user_services.register_house()
        return house_data
    except Exception as e:
        raise e

@alumni_bp.route("/course", methods=['POST'])
@jwt_required()
def register_programs():
    try:
        course_data = user_services.register_courses()
        return course_data
    except Exception as e:
        raise e


    