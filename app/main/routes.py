from __future__ import print_function
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request,  \
     current_app, session
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm, QuoteForm, EventForm
from app.models import User, Post, Quote, Event
from app.main import bp
from sqlalchemy import func
import pytz
import sys
from werkzeug.utils import secure_filename


@bp.context_processor
def inject_user():
    online_user = User.get_online_users()
    online_list = []
    for online in online_user:
        online_list.append(online.decode('utf-8')) 
    return dict(online_user=online_list)


@bp.context_processor
def inject_agenda():
    all_events = Event.all_events()
    event_list = []
    for item in all_events:
        event_list.append(item)
    return dict(agenda_list=event_list)


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        User.mark_online(current_user.username)
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None  
    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    quotes = user.quotez()
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None                  
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, quotes=quotes)


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
        filename = current_app.avatars.save(request.files["avatars"])
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


@bp.route('/enterquote', methods=['GET', 'POST'])
@login_required
def enterquote():
    form = QuoteForm()
    if form.validate_on_submit():
        quotedperson = User.query.filter(func.lower(User.username) == func.lower(form.name.data)).first()
        if quotedperson is None:
            flash("Please enter a valid user")
            return redirect(url_for('main.enterquote'))
        quote = Quote(quotedperson=quotedperson, body=form.quote.data)
        db.session.add(quote)
        db.session.commit()
        flash('Your quote has been succesfully added')
        return redirect(url_for('main.index'))
    return render_template('enterquote.html', title='Enter Quote', form=form)


@bp.route('/makeevent', methods=['GET', 'POST'])
@login_required
def makeevent():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(body=form.post.data, title=form.title.data,
                          location=form.location.data,
                          enroll=form.dropdown.data,
                          start_time=datetime.strptime(form.start_time.data, "%d/%m/%Y %H:%M"),
                          end_time=datetime.strptime(form.end_time.data, "%d/%m/%Y %H:%M"),
                          ev_time=form.ev_time.data)

        db.session.add(event)
        db.session.commit()
        flash('Your event has been created')
        return redirect(url_for('main.index'))
    return render_template('makeevent.html', title='Make Event', form=form)


@bp.route('/makepost', methods=['GET', 'POST'])
@login_required
def makepost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    return render_template('makepost.html', title='Make Post', form=form)


@bp.route('/eventlist')
@login_required
def eventlist():
    events = Event.query.order_by(Event.start_time).filter(Event.end_time >= datetime.now().date())
    local = pytz.timezone("Europe/Amsterdam")
    for item in events:
        item.start_time = local.localize(item.start_time, is_dst=None)
        print(item.start_time, sys.stderr)
    return render_template('eventlist.html', title='Event list', events=events)


@bp.route('/event/<event_id>')
@login_required
def event(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    if event.ev_time is not "":
        event.ev_time = datetime.strptime(event.ev_time, "%d/%m/%Y %H:%M")
    user = User.query.filter_by(username=current_user.username).first()
    participants = event.participants
    is_participating = event.check_participant(user)
    return render_template('eventlink.html', event=event, user=user, participants=participants, is_participating=is_participating, now=datetime.utcnow())


@bp.route('/enroll', methods=['GET', 'POST'])
@login_required
def enroll():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
    event = Event.query.filter_by(id=event_id).first_or_404()
    event.add_participant(current_user)
    db.session.commit()
    return redirect(url_for('main.event', event_id=event_id))


@bp.route('/unenroll', methods=['GET', 'POST'])
@login_required
def unenroll():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
    event = Event.query.filter_by(id=event_id).first_or_404()
    event.remove_participant(current_user)
    db.session.commit()
    return redirect(url_for('main.event', event_id=event_id))
