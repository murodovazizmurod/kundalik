from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

from datetime import datetime
from . import login_manager


@login_manager.user_loader
def user_loader(user_id):
    if 'login_type' in session:
        type = session['login_type']
        if type == 'student':
            return Student.query.get(int(user_id))
        if type == 'teacher':
            return Teacher.query.get(int(user_id))
    else:
        return False


subs = db.Table('subs',
                db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                )


class Teacher(db.Model, UserMixin):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    reg_date = db.Column(db.DateTime, default=datetime.now())
    role = db.relationship("Role", backref="teacher", lazy='dynamic')
    courses = db.relationship("Course", backref="teacher", lazy=True)
    last_active = db.Column(db.DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Teacher {self.name}"


class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    reg_date = db.Column(db.DateTime, default=datetime.now())
    course_id = db.relationship('Course', secondary=subs, backref=db.backref('students', lazy='dynamic'))
    last_active = db.Column(db.DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Student {self.name}"


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(255), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    room_number = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    start_time = db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"{self.name}"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    def __repr__(self):
        return f"{self.name}"


class Lessoon(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    course = db.relationship('Course', backref='lesson', lazy='dynamic')

    def __repr__(self):
        return f"Lesson {self.name}"


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    courses = db.relationship('Course', backref='room', lazy='dynamic')

    def __repr__(self):
        return f"Room №{self.number}"