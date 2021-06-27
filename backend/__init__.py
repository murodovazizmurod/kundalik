from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'slate'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name="English World Admin Panel", template_mode='bootstrap3', url='/adminpanel')
login_manager = LoginManager(app)

# Models
from . import models

admin.add_view(ModelView(models.Teacher, db.session))
admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Course, db.session))
admin.add_view(ModelView(models.Role, db.session))
admin.add_view(ModelView(models.Room, db.session))
admin.add_view(ModelView(models.Lessoon, db.session))
admin.add_view(ModelView(models.Post, db.session))

# BluePrints
from backend import classroom

classroom_blue = classroom.classroom

app.register_blueprint(blueprint=classroom_blue, url_prefix="/classroom")

from backend import main

main_blue = main.main

app.register_blueprint(blueprint=main.main)

from backend import auth

app.register_blueprint(blueprint=auth.auth, url_prefix="/Auth")
