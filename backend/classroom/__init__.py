from flask import Blueprint

classroom = Blueprint("class", __name__)

from .views import *
