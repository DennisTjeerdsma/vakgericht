from hashlib import md5
from time import time
from flask import current_app, flash
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from redis import Redis
from datetime import datetime


redis = Redis()

participants_table = db.Table('participants',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                              db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                              )

ACCESS = {
        "guest": 0,
        "user": 1,
        "vakblad": 2,
        "bestuur": 3,
        "admin": 4
        }


class User(UserMixin, db.Model):
    """ Class creating the User model in the database. The class has relationships to the Quote class, the Posts class
    and a many to many relationship with the events class. the many to many relationship is created through the
    participation_table. The class also contains several functions, these set passwords, reset passwords, mark the
    user as online, checks the user access level and several other functions."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    quotes = db.relationship('Quote', backref='quotedperson', lazy='dynamic')
    bday = db.Column(db.Date, default=datetime.utcnow)
    access = db.Column(db.String(64), default="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
        
    def quotez(self):
        return Quote.query.filter_by(user_id=self.id)
    
    def mark_online(user_id):
        now = int(time())
        expires = now + (current_app.config['ONLINE_LAST_MINUTES'] * 60) + 10
        all_users_key = 'online-users/%d' % (now // 60)
        user_key = 'user-activity/%s' % user_id
        p = redis.pipeline()
        p.sadd(all_users_key, user_id)
        p.set(user_key, now)
        p.expireat(all_users_key, expires)
        p.expireat(user_key, expires)
        p.execute()

    def get_user_last_activity(user_id):
        last_active = redis.get('user-activity/%s' % user_id)
        if last_active is None:
            return None
        return datetime.utcfromtimestamp(int(last_active))

    def get_online_users():
        current = int(time()) // 60
        minutes = range(current_app.config['ONLINE_LAST_MINUTES'])
        return redis.sunion(['online-users/%d' % (current - x)
                         for x in minutes])

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level: object) -> object:
        return self.access >= access_level
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    """Class that creates the database model for the posts group. All game descriptions and other posts are generated
    using  this class. The user_id functions for the relationship with the User class. This way, the author of the post
    is coupled to the users in the database. Every post gets assigned an id that functions an identifier for the posts.
    Other columns are the title, the body of the post and the timestamp at which the post was created.
    The language column is irrelevant for our application. """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def post_list(self):
        posts = Post.query.all()
        return posts.order_by(Post.timestamp.desc())


class Quote(db.Model):
    """Class that creates the database model for the quote system. The quote is coupled to users by a one to many
    relationship. The relationship is coupled to the User class by the user-id."""
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    name = db.Column(db.String(64),index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    
    def __repr(self):
        return '<Quote {}>'.format(self.body)


class Event(db.Model):
    """ The database model for the events class, this is the template in which all events are stored in the database.
    participants is a many-to-many relationship between the event and users registered in the event, this information
     this information is stored in the participants_table. The class contains several function which enroll or un-enroll
     participants to an event. The functions contain checks for enrollment closure and if the user is currently
     enrolled. There is also a function that queries the database for the agenda in the base.html."""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    title = db.Column(db.String(64))
    location = db.Column(db.String(64))
    enroll = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    end_time = db.Column(db.DateTime, default=datetime.now())
    start_time = db.Column(db.DateTime, default=datetime.now())
    ev_time = db.Column(db.String(64), default=datetime.utcnow())
    participants = db.relationship('User', secondary=participants_table, lazy='dynamic', backref=db.backref('participants', lazy=True))

    def add_participant(self, user):
        if datetime.strptime(self.ev_time, "%d/%m/%Y %H:%M") <= datetime.now():
            return flash("Enrollment has closed, please contact somebody from the board or \
            activities committee about enrolling.")
        elif self.check_participant(user):
            return flash('You are already enrolled')
        elif not self.check_participant(user):
            self.participants.append(user)
            return flash('You are now enrolled for this event')

    def remove_participant(self, user):
        if datetime.strptime(self.ev_time, "%d/%m/%Y %H:%M") <= datetime.now():
            return flash("Enrollment has closed, please contact somebody from the board or \
                        activities committee about un-enrolling.")
        elif self.check_participant(user):
            self.participants.remove(user)
            return flash('You are now unenrolled')

    def check_participant(self, user):
        return self.participants.filter(participants_table.c.user_id == user.id).count() > 0

    def get_participant(self):
        return User.query.filter(participants_table.c.event_id == self.id)

    @staticmethod
    def all_events():
        return Event.query.order_by(Event.start_time).filter(Event.end_time >= datetime.utcnow().date()).limit(10)


