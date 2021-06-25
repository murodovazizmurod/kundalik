from flask_login import current_user

from . import main


@main.route('/')
def index():
    return f'{current_user.is_authenticated}'