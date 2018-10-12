from flask_login import login_required, current_user
from flask import render_template, url_for, flash, redirect
from app import db
from app.main.forms import PostForm
from app.models import Post
from app.main import bp

@bp.route('/makepost', methods=['GET', 'POST'])
@login_required
def makepost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    return render_template('makepost.html', title='Make Post', form=form)