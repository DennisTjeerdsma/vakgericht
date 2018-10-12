from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main.routes import contextprocessor
from app.main.routes import index
from app.main.routes import user
from app.main.routes import editprofile
from app.main.routes import enterquote
from app.main.routes import makeevent
from app.main.routes import makepost
from app.main.routes import eventlist
from app.main.routes import event
from app.main.routes import enroll
from app.main.routes import unenroll
from app.main.routes import deleteavatar
