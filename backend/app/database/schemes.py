from enum import Enum
from pydantic import BaseModel, EmailStr
from flask_admin.contrib.sqla import ModelView
from typing import Optional
from wtforms import StringField
from wtforms.validators import DataRequired


class RoleEnum(Enum):
    admin = 'Mananges Settings, Users and Content'
    student = 'Create and Mange Personal Account and Content'
    house_master = 'Oversee and Manage House-Related Activities and Responsibility'


class RegisterUser(BaseModel):
    firstname:str
    lastname:str
    email: EmailStr
    password:str


class LoginUser(BaseModel):
    email:EmailStr
    password: str


class UpdateUser(BaseModel):
    email:Optional[EmailStr] = None
    password:Optional[str]= None
    


class CreateORUpdateCourse(BaseModel):
    title: str



class RoleView(ModelView):
    can_create= False
    can_delete= False
    can_edit= False
    

class UserView(ModelView):
    column_editable_list = ['approved', ]
    can_create= False
    can_delete = False
    column_filters = ['approved']
    can_export = True



class HouseView(ModelView):
    form_overrides = {
        'name': StringField,
    }
    form_args = {
        'name': {
            'validators': [DataRequired()]
        }
    }
    