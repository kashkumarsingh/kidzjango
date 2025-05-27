#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import Config, RepositoryEnv

def main():
    # Load .env file and set environment variables before importing settings
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        config = Config(RepositoryEnv(env_path))
        for key in config.repository.data:
            os.environ.setdefault(key, str(config.repository.data[key]))
    else:
        raise FileNotFoundError(f"Could not find .env file at {env_path}")

    # Set the settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()