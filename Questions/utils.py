import os
from django.conf import settings
import shutil
from django.core.cache import cache


def change_question_name(contest_name,previous_question_name,new_question_name):
    try:
        """This essentially changes the last question folder name with the new question name"""
        os.rename(
            os.path.join(settings.MEDIA_ROOT,
                               "contest",
                               contest_name,
                                previous_question_name
                                ),
            os.path.join(
                settings.MEDIA_ROOT,
                    "contest",
                    contest_name,
                    new_question_name,
                    ))
        return "Done"
    except OSError as e:
        print("Error Updating the folder name",e)
        return None
    

deleteCachedQuestions = lambda question : cache.delete(question) if cache.has_key(question) else None

def create_folder_for_questions(questions_name):
    path = os.path.join(settings.MEDIA_ROOT, f"Questions/{questions_name}")
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