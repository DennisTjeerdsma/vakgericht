from wtforms.widgets import TextArea
from wtforms import TextAreaField, TextField
from werkzeug.security import generate_password_hash

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


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
