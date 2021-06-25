from flask import render_template, request, url_for, flash, session
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import redirect

from . import auth
from .. import models, db


@auth.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('auth/index.html')
    else:
        return redirect(url_for('main.index'))


@auth.route('/student', methods=['GET', 'POST'])
def student():
    session['login_type'] = 'student'
    if not current_user.is_authenticated:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            if username and password:
                user = models.Student.query.filter_by(username=username).first()
                if user is not None and user.verify_password(password):
                    login_user(user, remember=True)
                    return redirect(url_for("main.index"))
                else:
                    flash('Invalid username or password!')
        return render_template('auth/student.html')
    return redirect(url_for("main.index"))


@auth.route('/teacher', methods=['GET', 'POST'])
def teacher():
    session['login_type'] = 'teacher'
    if not current_user.is_authenticated:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            if username and password:
                user = models.Teacher.query.filter_by(username=username).first()
                if user is not None and user.verify_password(password):
                    login_user(user, remember=True)
                    return redirect(url_for("main.index"))
                else:
                    flash('Invalid username or password!')
        return render_template('auth/teacher.html')
    return redirect(url_for("main.index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route("/signup", methods=["GET", "POST"])
def register():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            data = request.form
            user = models.Teacher(name=data['name'],
                                    username=data['username'],
                                    phone=data['phone'],
                                    email=data['email'],
                                    password=data['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.index'))
        else:
            return render_template('auth/simple.html')
    else:
        return redirect(url_for('main.index'))