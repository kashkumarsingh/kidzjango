"""
Development settings for the Kidz Runz Django project.

Extends base settings with configurations for local development.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Add development-specific apps
INSTALLED_APPS += [
    'django_browser_reload',  # For development hot reload
]

# Add development-specific middleware
MIDDLEWARE += [
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]