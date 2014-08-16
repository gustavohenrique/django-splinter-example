#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    APPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    sys.path.insert(0, APPS_DIR)

    TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    os.environ.setdefault("TEST_DISCOVER_TOP_LEVEL", TESTS_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
