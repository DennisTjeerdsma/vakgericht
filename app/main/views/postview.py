from flask_admin.contrib.sqla import ModelView
from app.main.views.fields import CKTextAreaField
from app.models import User, ACCESS
from flask_login import current_user

class PostView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            user = User.query.filter_by(username=current_user.username).first()
            return ACCESS[user.access] >= ACCESS["user"]
        else:
            return current_user.is_authenticated


    form_overrides = dict(
        body=CKTextAreaField,
    )

    create_template = 'admin.html'
    edit_template = 'admin.html'