from django.core.management.base import BaseCommand
import os
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Remove all migration files from all apps except __init__.py.'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        print(base_dir)
        apps_dir = os.path.join(base_dir)
        print(apps_dir)

        removed = []
        for app in os.listdir(apps_dir):
            migrations_path = os.path.join(apps_dir, app, 'migrations')
            if os.path.isdir(migrations_path):
                for fname in os.listdir(migrations_path):
                    if fname != '__init__.py' and fname.endswith('.py'):
                        fpath = os.path.join(migrations_path, fname)
                        os.remove(fpath)
                        removed.append(fpath)
                    elif fname.endswith('.pyc'):
                        fpath = os.path.join(migrations_path, fname)
                        os.remove(fpath)
                        removed.append(fpath)
        self.stdout.write(self.style.SUCCESS(f'Removed migration files:'))
        for f in removed:
            self.stdout.write(f'  {f}')
