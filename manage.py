#!/usr/bin/env python
""" Standard manage.py from django """
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DormitoryDollars.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
