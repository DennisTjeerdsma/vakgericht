from flask_login import login_required
from app.main.forms import EventForm
from flask import render_template, url_for, redirect, flash
from datetime import datetime
from app import db
from app.main import bp
from app.models import Event

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