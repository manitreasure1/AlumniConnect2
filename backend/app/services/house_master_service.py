
from sqlalchemy import select
from app.database.models import Users
from app.config.extensions import db
from flask import jsonify, make_response, redirect, url_for
from pprint import pprint

class HouseMasterServices:
    def approve_alumni(self, user_id):
        user = Users.get_user_by_id(user_id)
        user.approved = True # type: ignore
        db.session.commit()
        response = make_response("", 204)
        return response
       
        

    def reject_alumni(self, user_id):
        user = Users.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        response = make_response("", 204)
        return response
        
        

    def pending_approvals(self):
        users = Users.get_users()
        pending_users = [
            {
                "user_id": str(user.user_id),
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "username": user.username,
                "courses": [course.title for course in user.courses],
                "house": user.house.name if user.house_id else None,
            }
            for user in users if not user.approved
        ]
        response = make_response(jsonify({"pending_data": pending_users, "category":"seccess"}), 200)
        return response
        