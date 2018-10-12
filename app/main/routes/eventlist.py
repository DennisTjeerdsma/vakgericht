from flask_login import login_required
from app.models import Event
from flask import render_template, url_for
import pytz
from app.main import bp
from datetime import datetime

@bp.route('/eventlist')
@login_required
def eventlist():
    events = Event.query.order_by(Event.start_time).filter(Event.end_time >= datetime.now().date())
    local = pytz.timezone("Europe/Amsterdam")
    for item in events:
        item.start_time = local.localize(item.start_time, is_dst=None)
    return render_template('eventlist.html', title='Event list', events=events)