from functools import wraps
from app.models import ACCESS, User
from flask import redirect, flash, url_for
from flask_login import current_user


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(username=current_user.username).first()
            if ACCESS[user.access] < ACCESS[access_level]:
                flash("You do not have access to view this page.")
                return redirect(url_for("main.index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
