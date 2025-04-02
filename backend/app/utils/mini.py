from functools import wraps

from app.database.schemes import RoleEnum
from app.database.models import Role, Users
from app.config.extensions import db
from flask_jwt_extended import get_jwt_identity

def seed_initial_roles():
    for role in RoleEnum:
        new_roles = Role(title=role.name, activity=role.value) # type: ignore
        db.session.add(new_roles)
    db.session.commit()


def check_empty_roles():
    existing_role = Role.query.all()
    if not existing_role:
        seed_initial_roles()
   

def approved_user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = Users.get_user_by_id(get_jwt_identity())
        if user is None:
            raise PermissionError("User not found.")
        if not user.approved:
            raise PermissionError("User is not approved to access this resource.")
        return func(*args, **kwargs)
    return wrapper



def check_role(func):
    @wraps(func)
    def wrapper(role: list, *args, **kwargs):
        user = Users.get_user_by_id(get_jwt_identity())
        if user is None or user.role not in role:
            raise PermissionError("You do not have the required role to access this resource.")
        return func(role, *args, **kwargs)
    return wrapper