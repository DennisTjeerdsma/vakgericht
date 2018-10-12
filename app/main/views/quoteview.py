from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models import ACCESS, User


class QuoteView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            user = User.query.filter_by(username=current_user.username).first()
            return ACCESS[user.access] >= ACCESS["user"]
        else:
            return current_user.is_authenticated

    column_exclude_list = ("name")
    column_labels= dict(quotedperson="name")