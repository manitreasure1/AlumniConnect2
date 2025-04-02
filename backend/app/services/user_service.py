
from sqlalchemy import select
from app.config.extensions import db
from app.database.models import Users, Role, Course, House
from werkzeug.exceptions import NotFound
from flask import make_response, jsonify, request
from sqlalchemy import select
from flask_jwt_extended import get_jwt_identity


class UserService:
    def get_user_by_email(self, user_email):
        statement = db.session.execute(select(Users).where(Users.email == user_email))
        return statement.scalar_one_or_none()

    def existing_user(self, user_email):
        return self.get_user_by_email(user_email)
    
    def get_user_by_id(self, user_id):
        statement = db.session.query(Users).get(user_id)
        return statement
    
    def get_user_role(self, role_type:str):
        user_role = db.session.execute(select(Role).where(Role.title == role_type.lower()))
        role = user_role.scalar_one_or_none()
        if role is None:
            raise NotFound(f"{role_type} not found")
        return role.role_id
    
        
    def register_house(self):
        house_req = request.get_json()
        house_name = house_req.get('name')
        print(f"------------------------house-----name------------{house_name}")
        user_house = db.session.execute(select(House).where(House.name == house_name.title()))
        house = user_house.scalar_one_or_none()
        print(f"------------------------house--in db---------------{house}")
        if house is None:
            raise NotFound(f"{house_name} not found")
        
        user_obj = self.get_user_by_id(get_jwt_identity())
        if not user_obj:
            raise NotFound("User Not Found")
        user_obj.house_id = house.house_id
        db.session.commit()
        response = make_response(jsonify({
            "category": "success", "msg": f"You are now a member of {house.name}"
            }))
        return response
    
    def alumni_dashboard(self):
        userdb = self.get_user_by_id(get_jwt_identity())
        if not userdb:
            raise NotFound("User Not Found")         
        to_dict =  {
        "user_id": str(userdb.user_id),  
        "firstname": userdb.firstname,
        "lastname": userdb.lastname,
        "email": userdb.email,
        "courses": [course.title for course in userdb.courses],
        "role":userdb.role.title,
        "house":userdb.house.name if userdb.house_id else None,
        "approved": userdb.approved
        }
        return make_response(to_dict, 200)
    

    def register_courses(self):
        course_req = request.get_json()
        course_ids = course_req.get("course_ids", [])
        if not course_ids:
            return make_response(jsonify({"msg": "No courses selected", "category": "danger"}), 400)
        user = self.get_user_by_id(get_jwt_identity())
        if not user:
            return make_response(jsonify({"msg": "User not found", "category": "danger"}), 404)
        courses = db.session.query(Course).filter(Course.course_id.in_(course_ids)).all()
        if not courses:
            return make_response(jsonify({"msg": "No valid courses found", "category": "danger"}), 400)
        user.courses.extend(courses)
        db.session.commit()
        return make_response(jsonify({
            "msg": "Courses registered successfully",
            "category": "success",
            "courses": [course.title for course in courses]
        }), 200)

        
    
        

    

    

