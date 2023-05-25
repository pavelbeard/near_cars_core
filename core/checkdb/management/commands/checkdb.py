import sys
import time

from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

help_string = "Проверяет подключение к базе данных."


class Command(BaseCommand):
    help = help_string

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            nargs='?',
            type=str,
            help="Имя подключения к базе данных, определенное в <корень_приложения>/settings.py."
        )
        parser.add_argument(
            '--seconds',
            nargs='?',
            type=int,
            help="Ожидание следующей попытки подключения в секундах. По умолчанию - 5 секунд.",
            default=5
        )
        parser.add_argument(
            '--retries',
            nargs='?',
            type=int,
            help="Количество попыток подключения к БД. По умолчанию - 3.",
            default=3
        )

    def handle(self, *args, **options):
        wait, retries, database = options['seconds'], options['retries'], options['database']
        self.stdout.write(f"Wait for connection to the database {database}...")
        conn = None

        att = 0
        for attempt in range(retries):
            try:
                db_conn = connections[database]
                db_conn.cursor()
                conn = True
                break
            except OperationalError:
                self.stdout.write(f"Connection attempt {database}...")
                time.sleep(wait)
                conn = False
                att += 1

        if conn:
            self.stdout.write(self.style.SUCCESS(f"Successful connection to {database} database!"))
        else:
            self.stdout.write(self.style.ERROR(f"The database {database} isn't responding after {att} connection "
                                               f"attempts"))
            sys.exit(1)


Command.__doc__ = help_string
