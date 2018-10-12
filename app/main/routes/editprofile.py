from flask_login import login_required, current_user
from app.main.forms import EditProfileForm
from app.models import User
from flask import render_template, url_for, current_app, flash, request, redirect
from app.main import bp
import time
from werkzeug.utils import secure_filename

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    user_input = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        if form.password.data != "":
            current_user.set_password(form.password.data)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        current_user.club = form.club.data
        current_user.study = form.study.data
        filename = current_app.avatars.save(request.files["uploadFile"], name=current_user.username + str(time.time())+".")
        current_user.avatar = secure_filename(filename)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
        form.study.data = current_user.study
        form.club.data = current_user.club
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user_input)