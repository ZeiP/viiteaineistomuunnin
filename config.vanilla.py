# Enable Flask's debugging features. Should be False in production
ENV = 'development'
DEBUG = True
SECRET_KEY = 'SECRET_KEY_HERE'
UPLOAD_FOLDER = '/tmp'
SMTP_SERVER = 'localhost'
FEEDBACK_TO = 'feedback@example.org'
EMAIL_FROM = 'webmaster@example.org'
