from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drops and recreates the public schema in the database (PostgreSQL only).'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('DROP SCHEMA public CASCADE;')
            cursor.execute('CREATE SCHEMA public;')
        self.stdout.write(self.style.SUCCESS('Database schema public dropped and recreated.'))
