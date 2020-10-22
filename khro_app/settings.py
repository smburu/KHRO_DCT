"""
This is a Django settings for KHRO datacapture tool (DCT) developed for thr Ministry of Health (Kenya).

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY KEY: The secret key has beek kept secret in a location outside the app base directory!
SECRET_KEY = '3$^b$=-@27(xi&dn65jw0f3=qmx=m&uog-s2=_tx6y&4s$_pu8'

DEBUG =True

ALLOWED_HOSTS = os.getenv(
    'KHRO_ALLOWED_HOSTS', 'localhost,127.0.0.1,khro-dct.health.go.ke').split(',')

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 # This should higher than the default 1000 fields

# Application definition
INSTALLED_APPS = [
    'admin_menu', #this is a plug-in app in site_packages used to provide horizontal menu bar
    'admin_reorder',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # register Django REST
    'rest_framework_swagger',
    'data_wizard', #register data import wizard
    'data_wizard.sources',  # Optional registration but important
    'import_export', #for inport and export functions
    'khro_app.home', #installed startup AHO data capture app that calls all other modules
    'khro_app.authentication',
    'khro_app.indicators',
    'khro_app.regions',
    'khro_app.elements',
    'khro_app.research',
    'khro_app.commodities',
    'khro_app.common_info',
    'django_admin_listfilter_dropdown',
	'bandit', #jsut for testing email sending ...will be removed during full deployment

]

# This can be omitted to use the defaults
DATA_WIZARD = {
    'BACKEND': 'data_wizard.backends.threading',
    'LOADER': 'data_wizard.loaders.FileLoader',
    'PERMISSION': 'rest_framework.permissions.IsAdminUser',
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',

    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '10000/day',
        'anon': '10000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DATETIME_FORMAT': 'iso-8601',
    'DATE_FORMAT': 'iso-8601',
    'TIME_FORMAT': 'iso-8601',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'khro_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'khro_app/templates') #templates are located inside the project directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'khro_app.wsgi.application'

# Database settings to connect to MySQL databases admin and data repository
DATABASES = {
   'default': {   # this is the legacy database
       'ENGINE': 'django.db.backends.mysql',
       'NAME': os.getenv('KHRO_DATABASE', 'khrodct_database'),
       'OPTIONS': {
          'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       'USER': os.getenv('KHRO_DATABASE_USER', 'root'),
       'PASSWORD': os.getenv('KHRO_DATABASE_PASSWORD', 'Aho@1234'),
       'HOST': 'localhost',
       'PORT': '3306',
   },
}

# custom user authentication and Password validation settings must be set to avaid error such as:
# clashes with reverse accessor for 'CustomUser
AUTH_USER_MODEL = 'authentication.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True
USE_L10N = True

USE_TZ = True
IMPORT_EXPORT_USE_TRANSACTIONS=True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'khro_app/static/')
]
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR + STATIC_URL)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'khro_app/repository/') # 'data' is my media folder

ADMIN_LOGO = 'logo2.png' #display the AHO logo on the login screen and admin page

#This is a custome blue theme for the site can be changed to any other as per country preferrences
AADMIN_STYLE = {
    'primary-color': '#2B3746',
    'secondary-color': '#354151',
    'tertiary-color': '#F2F9FC'
}
LOGOUT_REDIRECT_URL='/'

ADMIN_REORDER = (
    # Keep original label and models
    'home',
    'indicators',
    'research',
    {'app': 'elements', 'label': 'Raw Data Elements'},
	{'app': 'regions', 'label': 'Counties Profile'},
    {'app': 'authentication', 'label': 'User and Group Permissions'},
)

#for testing email sending for purpose of password reset
EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aho.stevenwho@gmail.com'
EMAIL_HOST_PASSWORD = 'mburu1234'
EMAIL_PORT = 587

BANDIT_EMAIL = ['smburu@mtccl.co.ke','aho.stevenwho@gmail.com','libokognekabassad@who.int','ilboudod@who.int','nshimirimanaj@who.int']
