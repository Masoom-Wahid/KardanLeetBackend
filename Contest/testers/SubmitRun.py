from .execute import RunCode
import secrets
from Contest.models import Contest_submissiosn
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from Contest.tasks import scheduler
from ..utils import getLeaderBoardData,sortLeaderBoarddata
import uuid


class SubmitRun(RunCode):
    def __init__(self,group,question,contest,language,file):
        super().__init__(group,question,contest,language,file)
        self.LeaderBoardDealy = timezone.now() + timedelta(seconds=2)
        self.obj = Contest_submissiosn.objects.create(
            id = uuid.uuid4(),
            group = group,
            question = question,
            lang=language,    
            code = "",
            status="",
            submit_time = self.getsubmitTime()
        )
        self.group = group
        self.file = file
        self.num_of_test_cases=question.num_of_test_cases
        self.manual_testCase = None

    """For Getting The Submit Time Of The User"""
    getsubmitTime = lambda self :   (timezone.now() - self.group.contest.started_at).total_seconds()

    def makeId(self):
        # token = secrets.token_urlsafe(6)
        # while Contest_submissiosn.objects.filter(id=token).exists():
        #     token = secrets.token_urlsafe(6)
        # return token
        return uuid.uuid4()


    def updateLeaderboard(self,instance):
        leaderboard_obj = cache.get("leaderboard")
        if leaderboard_obj != None:
            leaderboard_obj[self.group.group_name] = self.group.calculateResults()
            cache.set("leaderboard",leaderboard_obj,14400)
        else:
            leaderboard_obj = getLeaderBoardData(self.group.contest)
            cache.set("leaderboard",leaderboard_obj,14400)
   

    def writeCode(self,file):
        self.obj.code = file
        self.obj.save()
    
    def setStatus(self,status):
        if status == "Solved":
            self.obj.solved = True
        self.obj.status=status
        scheduler.add_job(self.updateLeaderboard, 'date',[self.obj], run_date=self.LeaderBoardDealy,id=self.obj.id)
        self.obj.save()



    def makethefile(self, file_code, suffix):
        _,__,code =  super().makethefile(file_code, suffix)
        self.writeCode(code)
        return _,__,code
        
    def run(self):
        result, details = super().run()
        if result:
            self.setStatus("Solved")
        else:
            self.setStatus(details["reason"])

        return result,details