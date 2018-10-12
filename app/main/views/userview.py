from werkzeug.utils import secure_filename
from app.models import ACCESS, User
from app.main.views.fields import MyPassField 
import time
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
import os.path as op
from flask import current_app
from flask_admin.form.upload import ImageUploadField


class UserView(ModelView):

    def on_model_change(self, form, model, is_created):
        self.username = model.username

        if model.avatar is None:
            model.avatar = "vakgericht.jpeg"

    def prefix_name(self, file_data):
        parts = op.splitext(file_data.filename)
        return secure_filename(str(self.username) + str(time.time()) + str(parts[1]))

    form_overrides = dict(
        password_hash=MyPassField,
        avatar=ImageUploadField,
    )

    form_widget_args = dict(
        password_hash=dict(
            placeholder='Enter new password here to change password',
        ),
    )

    form_args = {
        'avatar': {
            "label": "Avatar",
            "base_path": current_app.config["UPLOADED_AVATARS_DEST"],
            "url_relative_path": "./avatars/",
            "namegen": prefix_name,
        }
    }

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
