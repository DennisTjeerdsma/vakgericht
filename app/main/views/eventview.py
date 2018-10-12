from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models import User, ACCESS


class EventView(ModelView):
    def is_accessible(self):
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