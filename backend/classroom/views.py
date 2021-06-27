from flask import render_template, session, redirect, url_for, abort
from flask_login import login_required, current_user

import datetime, calendar

from . import classroom
from ..models import Post, Course, Room


@classroom.route('/')
@login_required
def index():
    if session['login_type'] == 'teacher':
        return redirect(url_for('class.teacher'))
    if session['login_type'] == 'student':
        return redirect(url_for('class.student'))


@classroom.route('/teacher')
@login_required
def teacher():
    if session['login_type'] == 'teacher':
        now = datetime.datetime.now()
        data = {}
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        lessons = Course.query.filter(Course.teacher == current_user).filter(Course.start_time >= now).filter(Course.start_time <= tomorrow).all()
        posts = Post.query.all()

        if len(posts) == 0:
            posts = False
        if posts:
            data['post'] = {
                'name': posts[-1].name,
                'time': posts[-1].published_at,
                'text': posts[-1].text,
                'author': posts[-1].teacher.name
            }
            data['today_lessons'] = [i for i in lessons]
        return render_template('classroom/teacher.html', data=data)

    return redirect(url_for('class.index'))


@classroom.route('/teacher/calendar')
@login_required
def teacher_calendar():
    if session['login_type'] == 'teacher':
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        
        num_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
        end = datetime.date(year, month, num_days)
        lessons = Course.query.filter(Course.start_time >= now).filter(Course.start_time < end).all()
        students = 0
        courses = []
        for i in lessons:
            students += len(i.students)
            if not i.lesson in courses:
                courses.append(i.lesson)
        return render_template('classroom/teacher_calendar.html', days=days, now=now, lessons=lessons, students=students, courses=courses)

    return redirect(url_for('class.index'))


@classroom.route('/teacher/calendar/<time>')
@login_required
def teacher_calendar_day(time):
    if session['login_type'] == 'teacher':
        data = {
            'rooms': Room.query.all(),
            'time': time
        }

        return render_template('classroom/teacher_calendar_room.html', data=data)

    return redirect(url_for('class.index'))


@classroom.route('/teacher/calendar/<time>/<int:room>')
@login_required
def teacher_calendar_day_room(time, room):
    if session['login_type'] == 'teacher':
        try:
            year = int(time.split('.')[2])
            month = int(time.split('.')[1])
            day = int(time.split('.')[0])
            start = datetime.date(year, month, day)
            end = start + datetime.timedelta(days=1)
        except Exception:
            return abort(400)
        courses = Course.query.filter(Course.start_time >= start).filter(Course.start_time <= end).filter(Course.room_number == room).all()

        data = {
            'courses': courses,
            'date': time
        }

        return render_template('classroom/teacher_calendar_room_day.html', data=data)

    return redirect(url_for('class.index'))


# Student
@classroom.route('/student')
@login_required
def student():
    if session['login_type'] == 'student':
        return render_template('classroom/student.html')

    return redirect(url_for('class.index'))