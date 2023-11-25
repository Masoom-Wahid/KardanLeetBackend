import os
from django.conf import settings
import shutil
def create_folder_for_contest(contest_name):
    path = os.path.join(settings.MEDIA_ROOT, f"contest/{contest_name}")
    try:
        os.makedirs(path, exist_ok=True)
        print("---Created A Dir For The Contest---")
    except OSError as e:
        print("Error creating dirs", e)
        return
    

def delete_folder_for_contest(contest_name):
    path = os.path.join(settings.MEDIA_ROOT, f"contest/{contest_name}")
    print(path)
    contents = os.listdir(path)
    print(contents)
    if not contents:
        os.rmdir(path)
    else:
        shutil.rmtree(path)
    