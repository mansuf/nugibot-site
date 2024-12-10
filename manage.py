#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import json

with open("secrets/aws-cognito-client-secret.txt", "r") as o:
    os.environ.setdefault("AWS_COGNITO_CLIENT_SECRET", o.read())

with open("secrets/secret-key.txt", "r") as o:
    os.environ.setdefault("SECRET_KEY", o.read())

with open("secrets/mysql-database.json") as o:
    data = json.loads(o.read())

    for key, value in data.items():
        os.environ.setdefault(key, value)

with open("secrets/storage-s3.json", "r") as o:
    data = json.loads(o.read())

    for key, value in data.items():
        os.environ.setdefault(key, value)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nugitechsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
