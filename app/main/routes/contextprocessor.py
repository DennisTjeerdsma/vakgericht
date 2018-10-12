from app.models import User, Event
from flask_login import current_user
from app import db
from app.main import bp
from datetime import datetime

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