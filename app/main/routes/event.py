from flask_login import login_required, current_user
from app.models import Event, User
from flask import render_template
from datetime import datetime
from app.main import bp

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