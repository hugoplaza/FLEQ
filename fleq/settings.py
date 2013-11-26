# Django settings for fleq project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('FLEQ Admin', 'fleq@libresoft.es'), 
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fleq_db',  			# Or path to database file if using sqlite3.
        'USER': 'root',                      	# Not used with sqlite3.
        'PASSWORD': 'cris.5033',                  	# Not used with sqlite3.
        'HOST': '',                      	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      	# Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'Europe/Brussels'
TIME_ZONE = ''


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/srv/wwwmedia/media.lawrence.com/"
#MEDIA_ROOT = '/srv/www/FLEQ/fleq/template/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/srv/wwwmedia/media.lawrence.com/static/"
#STATIC_ROOT = '/srv/www/FLEQ/fleq/'
STATIC_ROOT = ''



# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

ADMIN_MEDIA_PREFIX = '/admin/media/'


# Email configuration
# EMAIL_USE_TLS = True                                          
# EMAIL_HOST = 'mailer.libresoft.es'                                 
# EMAIL_HOST_USER = 'fredondo@libresoft.es'                        
# EMAIL_HOST_PASSWORD = 'mod.welor.210904'                            
# EMAIL_PORT = 587

# Email configuration
#EMAIL_USE_TLS = True                                          
#EMAIL_HOST = 'mailer.libresoft.es'                                 
#EMAIL_HOST_USER = 'fleq-lite@libresoft.es'                        
#EMAIL_HOST_PASSWORD = 'fleq-lite'                            
#EMAIL_PORT = 587                                         


# Temporary email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fleq.libresoft@gmail.com'
EMAIL_HOST_PASSWORD = 'A1b2C3d4E5'
EMAIL_PORT = 587


# Make this unique, and don't share it with anybody.
SECRET_KEY = ')2-q1^z&u@ch0)7tq!h+6vu9xy#h1lr1v5g(41i66*f(w&lb&c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fleq.minidetector.Middleware',
)




ROOT_URLCONF = 'fleq.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/srv/wwwhtml/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	'template',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',   
    'fleq.quizbowl',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


AUTH_PROFILE_MODULE = 'quizbowl.Player'
