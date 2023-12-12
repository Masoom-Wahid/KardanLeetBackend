from .models import Contests
class Leaderboard:
    def createLeaderBoard(self,contest):
        return {contestant.group_name : {
            "id":contestant.id,
            "points":0,
            "time":0,
            "penalty":0,
        } for contestant in contest.contest_groups_set.all() }

    def __init__(self,contest):
        self.leaderboardRanking = self.createLeaderBoard(contest)
        self.contest = contest


    def printLeaderBoard(self):
        print(self.leaderboardRanking)

    def updateLeaderBoard(self,groupName,groupObj):
       print(groupName)
       self.leaderboardRanking[groupName]={
        "id": groupObj.id,
        "points" : groupObj.calculateTotalPoint(),
        "time":groupObj.calculateTime(),
        "penalty":groupObj.calculatePenalty(),
       }
       print(self.leaderboardRanking)
       
    def sortLeaderBoard(self):
        self.leaderboardRanking = sorted(self.leaderboardRanking,
                                         key=lambda contestant :(contestant["points"],contestant["time"]))
        
