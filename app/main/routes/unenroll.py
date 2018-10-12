from app.main import bp
from flask_login import login_required, current_user
from flask import request, redirect, url_for
from app.models import Event
from app import db


@bp.route('/unenroll', methods=['GET', 'POST'])
@login_required
def unenroll():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
    event = Event.query.filter_by(id=event_id).first_or_404()
    event.remove_participant(current_user)
    db.session.commit()
    return redirect(url_for('main.event', event_id=event_id))