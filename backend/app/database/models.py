from app.config.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
import uuid
from typing import List



users_courses = db.Table(
    "users_courses",
    db.Column("user_id", ForeignKey("users.user_id"), primary_key=True),
    db.Column("course_id", ForeignKey("course.course_id"), primary_key=True),
)

class Users(db.Model):
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email:Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash:Mapped[str]
    approved:Mapped[bool] = mapped_column(default=False)

    role:Mapped['Role'] = relationship("Role", back_populates='users')
    house: Mapped['House'] =  relationship("House", back_populates='users')
    courses: Mapped[List['Course']] = relationship('Course', secondary=users_courses, back_populates='users')

    role_id: Mapped[UUID|None] = mapped_column(ForeignKey('role.role_id'), nullable=True)
    house_id: Mapped[UUID|None] = mapped_column(ForeignKey('house.house_id'), nullable=True)

    @staticmethod
    def get_user_by_id(user_id:str):
        user_obj = db.session.get(Users, user_id)
        return user_obj
    
    @staticmethod
    def get_users():
        return db.session.query(Users).all()


class Role(db.Model):
    role_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    activity: Mapped[str] = mapped_column(String(150))

    users: Mapped[List['Users']]= relationship("Users", back_populates='role')


class House(db.Model):
    house_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(55), index=True, unique=True)

    users:Mapped[List['Users']] = relationship("Users", back_populates='house')


class Course(db.Model):
    course_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] =  mapped_column(String(100), index=True)

    users:Mapped[List['Users']] = relationship("Users", secondary=users_courses,  back_populates='courses')
