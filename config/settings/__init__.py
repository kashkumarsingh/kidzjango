import os

# Determine the environment and import the appropriate settings
environment = os.getenv('DJANGO_ENV', 'development')
if environment == 'production':
    from .production import *  # noqa
else:
    from .development import *  # noqa