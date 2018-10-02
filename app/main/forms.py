from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from app.models import User
from datetime import datetime
from flask_wtf.file import FileField, FileAllowed
import os


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    """
    field_flags = ('requiredif',)

    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    """field is requiring that name field in the form is data value in the form"""
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    email = StringField("Email", validators=[DataRequired()])
    birthday = StringField("Birthday", id="datepicker", validators=[DataRequired()])
    club = StringField("Previous club", validators=[Length(min=0, max=128)])
    avatar = FileField("Avatar", validators=[FileAllowed(current_app.avatars, "images only!")])
    study = StringField("Studying", validators=[Length(min=0, max=128)])
    password = PasswordField("Password", validators=[Length(min=0, max=20)])
    password2 = PasswordField("Repeat Password", validators=[Length(min=0, max=20), RequiredIf("password")])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_password(self, password):
        if password.data != "" and password.data != self.password2.data:
            raise ValidationError("Password's must match")

    def validate_email(self, email):
        original_email = User.query.filter_by(username=self.original_username).first().email
        if email.data != original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError("Email is in use, please pick a different email")

    def validate_avatar(self, avatar):
        user = User.query.filter_by(username=self.original_username).first()
        if avatar.data is None:
            return
        if user.avatar is not "vakgericht.jpeg" \
                and os.path.isfile(os.path.join(current_app.config["UPLOADED_AVATARS_DEST"], user.avatar)):
            os.remove(os.path.join(current_app.config["UPLOADED_AVATARS_DEST"], user.avatar))




class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QuoteForm(FlaskForm):
    quote = TextAreaField('Enter a Quote', validators=[DataRequired(), Length(min=1, max=140)])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1,max=140)])
    post = TextAreaField('Description', validators=[Length(min=0, max=500)])
    location = StringField('Location', validators=[Length(min=0)])
    dropdown = SelectField(choices=[("No", "No"), ("Yes", "Yes")], id="dropdown", validators=[DataRequired()])
    start_time = StringField('Event start', id='datetimepicker1', validators=[DataRequired()])
    end_time = StringField('Event end', id='datetimepicker2', validators=[DataRequired()])
    ev_time = StringField('Enrollment closed', id='datetimepicker3', validators=[RequiredIf(dropdown="Yes")])
    submit = SubmitField('Submit')

    def validate_end_time(self, args):
        if self.end_time.data is None or self.start_time is None or self.ev_time is None:
            return
        if datetime.strptime(self.end_time.data, '%d/%m/%Y %H:%M') < datetime.strptime(self.start_time.data, '%d/%m/%Y %H:%M'):
            raise ValidationError('End time cannot be before start time')
    
    def validate_ev_time(self, args):
        if self.end_time.data is None or self.start_time is None or self.ev_time is None:
            return
        if datetime.strptime(self.ev_time.data, '%d/%m/%Y %H:%M') > datetime.strptime(self.start_time.data, '%d/%m/%Y %H:%M'):
            raise ValidationError('Enrollment cannot close after event has started')

