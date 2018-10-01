import os
from dotenv import load_dotenv
from redis import Redis

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

redis = Redis()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    POSTS_PER_PAGE = 25
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ONLINE_LAST_MINUTES = 5
    MY_DATE_FORMATS= ['%d/%m/%y']


    """Configuring uploads"""
    UPLOADS_DEFAULT_DEST = './Images/Avatars'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/'

    UPLOADED_IMAGES_DEST = "./Images/Avatars"
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'