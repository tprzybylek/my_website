from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@3a19^v$#1)3q#a7e0z+rr0(notc6hf!5@)8!^_td!ykcw$j*e'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost', '.localhost', 'tprzybylek.me', '.tprzybylek.me', '46.101.159.58']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
