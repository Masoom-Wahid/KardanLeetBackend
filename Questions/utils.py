import os
from django.conf import settings
import shutil
def create_folder_for_questions(contest_name,questions_name):
    print(questions_name)
    path = os.path.join(settings.MEDIA_ROOT, f"contest/{contest_name}/{questions_name}")
    try:
        os.makedirs(path, exist_ok=True)
        print("---Created A Dir For The Question---")
    except OSError as e:
        print("Error creating dirs", e)
        return
    
def delete_folder_for_contest(contest_name,question_name):
    path = os.path.join(settings.MEDIA_ROOT, f"contest/{contest_name}/{question_name}")
    contents = os.listdir(path)
    try:
        if not contents:
            os.rmdir(path)
        else:
            shutil.rmtree(path)
    except OSError as e:
        print("Error deleting the dir ",e)
        return