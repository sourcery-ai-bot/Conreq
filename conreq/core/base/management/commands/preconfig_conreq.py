import os
import shutil
import sqlite3
import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from conreq.utils.environment import get_database_type, get_debug

DEBUG = get_debug()
BASE_DIR = getattr(settings, "BASE_DIR")
DATA_DIR = getattr(settings, "DATA_DIR")
DATABASES = getattr(settings, "DATABASES")
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


class Command(BaseCommand):
    """Executes functions that may require admin privileges,
    since it is expected that run_conreq is executed as a user."""

    help = "Runs code that may be required prior to run_conreq Conreq."

    def handle(self, *args, **options):
        uid = options["uid"]
        gid = options["gid"]
        no_perms = options["no_perms"]

        print("Preconfiguring Conreq...")

        # Django database
        if get_database_type() == "SQLITE3":
            database = DATABASES["default"]["NAME"]
            self.setup_sqlite_database(database, "Conreq", uid, gid, no_perms)

        # Background task database
        if HUEY_FILENAME:
            self.setup_sqlite_database(
                HUEY_FILENAME, "Background Task", uid, gid, no_perms
            )

        if DEBUG:
            # Migrate silk due to their wonky dev choices
            call_command("makemigrations", "silk")

        if not no_perms and sys.platform == "linux":
            # Conreq data dir
            self.recursive_chown(DATA_DIR, uid, gid)

            # Conreq core dir
            self.recursive_chown(BASE_DIR, uid, gid)

    def add_arguments(self, parser):
        parser.add_argument(
            "uid",
            nargs="?",
            help="User ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )
        parser.add_argument(
            "gid",
            nargs="?",
            help="Group ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )

        parser.add_argument(
            "--no-perms",
            action="store_true",
            help="Prevent Conreq from setting permissions.",
        )

    @staticmethod
    def setup_sqlite_database(path, name, uid, gid, no_perms):
        print(name.rstrip(" ") + " Database")
        if not os.path.exists(path):
            print("> Creating database")
        with sqlite3.connect(path) as cursor:
            print("> Vacuuming database")
            cursor.execute("VACUUM")
            print("> Configuring database")
            cursor.execute("PRAGMA journal_mode = WAL;")
        if not no_perms and (uid != -1 or gid != -1) and sys.platform == "linux":
            # pylint: disable=no-member
            print("> Applying permissions")
            new_uid = uid or os.getuid()
            new_gid = gid or os.getgid()
            os.chown(path, new_uid, new_gid)
        print("> Complete")

    @staticmethod
    def recursive_chown(path, uid, gid):
        print('Recursively applying permissions to "' + path + '"')
        new_uid = uid if uid != -1 else None
        new_gid = gid if gid != -1 else None
        if uid != -1 or gid != -1:
            # pylint: disable=unused-variable
            for dirpath, dirnames, filenames in os.walk(path):
                try:
                    shutil.chown(dirpath, new_uid, new_gid)
                    try:
                        for filename in filenames:
                            shutil.chown(
                                os.path.join(dirpath, filename), new_uid, new_gid
                            )
                    except FileNotFoundError:
                        print(
                            'Unable to apply permissions to "'
                            + os.path.join(dirpath, filename)
                            + '". File not found.'
                        )
                except PermissionError:
                    print(
                        'Unable to apply permissions to "'
                        + dirpath
                        + '". Permission denied.'
                    )
