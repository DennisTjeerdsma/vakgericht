from flask_admin.contrib.sqla import ModelView
from app.models import User, ACCESS, Event
from wtforms import TextField
from werkzeug.security import generate_password_hash
from flask_login import current_user


class MyPassField(TextField):
    def process_data(self, value):
        self.data = ''  # even if password is already set, don't show hash here
        self.orig_hash = value

    def process_formdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        if value:
            self.data = generate_password_hash(value)
        else:
            self.data = self.orig_hash


class UserView(ModelView):
    form_overrides = dict(
        password_hash=MyPassField,
    )
    form_widget_args = dict(
        password_hash=dict(
            placeholder='Enter new password here to change password',
        ),
    )

    def is_accessible(self):
        if current_user.is_authenticated:
            user = User.query.filter_by(username=current_user.username).first()
            return ACCESS[user.access] >= ACCESS["bestuur"]
        else:
            return current_user.is_authenticated

    column_exclude_list = ("password_hash", "about_me")
    column_labels = dict(bday="Birthday", access="Access Level", password_hash="Password")
    form_excluded_columns = ["posts", "last_seen", "quotes", "followers", "followed", "participants"]

    form_choices = {
        "access": [
            ("guest", "guest"),
            ("user", "user"),
            ("vakblad", "vakblad"),
            ("bestuur", "bestuur"),
            ("admin", "admin")
        ]
    }


class EventView(ModelView):
    def is_accessible(access_level):
        if current_user.is_authenticated:
            user = User.query.filter_by(username=current_user.username).first()
            return ACCESS[user.access] >= ACCESS["bestuur"]
        else:
            return current_user.is_authenticated

    column_list = ("title", "location", "enroll", "start_time", "end_time", "ev_time")
    column_labels = dict(title="Name", enroll="Enroll [Yes/No]", ev_time="Enrollment closes", body="Description")
    form_columns = ["title", "location", "body", "enroll", "start_time", "end_time",
                    "ev_time", "participants"]

    form_choices = {
        "enroll": [
            ("No", "No"),
            ("Yes", "Yes")
        ]
    }
