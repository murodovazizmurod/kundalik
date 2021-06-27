from flask import render_template

from . import main
from ..models import Student, Course


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/student/<string:username>')
def profile(username):
    user = Student.query.filter_by(username=username).first_or_404()
    if not user is None:
        data = {
            'name': user.name,
            'username': user.username,
            'last': user.last_active.strftime('%H:%M %d.%m.%y'),
            'reg_date': user.reg_date.strftime('%H:%M %d.%m.%y') 
        }
    return render_template('main/user.html', data=data)


@main.route('/course/<int:id>')
def course_info(id):
    course = Course.query.filter_by(id=id).first_or_404()
    if not course is None:
        data = {
            'name': course.lesson.name,
            'teacher': course.teacher,
            'start_time': course.start_time,
            'room': course.room,
            'students': len(course.students)
        }
    return render_template('main/course.html', data=data)

