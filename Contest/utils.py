import os
from django.conf import settings
import shutil
from collections import OrderedDict
from .models import Contests


def sortLeaderBoarddata(data):
    sorted_data = OrderedDict(sorted(data.items(), key=lambda x: (-x[1]['point'], x[1]['time'] + x[1]["penalty"])))
    return sorted_data

def getLeaderBoardData(contest):
    groups = contest.contest_groups_set.all()
    result = {}
    for group in groups:
        result[group.group_name] = {
            "id":group.id,
            "point":group.calculateTotalPoint(),
            "time":group.calculateTime(),
            "penalty":group.calculatePenalty()
        }
    return result

def change_contest_name(previous_contest_name,new_contest_name):
    try:
        """This essentially changes the last contest folder name with the new contest name"""
        os.rename(
            os.path.join(settings.MEDIA_ROOT,
                               "contest",
                               previous_contest_name,
                                ),
            os.path.join(
                settings.MEDIA_ROOT,
                    "contest",
                    new_contest_name,
                    ))
        return "Done"
    except OSError as e:
        print("Error Updating the folder name",e)
        return None
    
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
    contents = os.listdir(path)
    if not contents:
        os.rmdir(path)
    else:
        shutil.rmtree(path)
    