from .execute import RunCode
import secrets
from Contest.models import Contest_submissiosn
from django.utils import timezone
from datetime import timedelta
from django.core import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from Contest.tasks import scheduler

class SubmitRun(RunCode):
    def __init__(self,group,question,contest,language,file):
        super().__init__(group,question,contest,language,file)
        self.LeaderBoardDealy = timezone.now() + timedelta(seconds=2)
        self.obj = Contest_submissiosn.objects.create(
            id = self.makeId(),
            group = group,
            question = question,
            lang=language,    
            code = "",
            status=""
        )
        self.file = file
        self.num_of_test_cases=question.num_of_test_cases
        self.manual_testCase = None

    def makeId(self):
        token = secrets.token_urlsafe(16)
        while Contest_submissiosn.objects.filter(id=token).exists():
            token = secrets.token_urlsafe(16)
        return token

    def updateLeaderboard(self,instance):
        leaderboard_obj = cache.get("leaderboard")
        if leaderboard_obj != None:
            
            stats = {
                "id":self.group.id,
                "point":self.group.calculateTotalPoint(),
                "time":self.group.calculateTime(),
                "penalty":self.group.calculatePenalty()
            }
            leaderboard_obj[self.group.group_name] = stats
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("leaderboard", {"type": "Leaderboard.update","update":leaderboard_obj})
        else:
            pass        

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