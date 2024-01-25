from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
QUESTION_LEVELS = [
    ("EASY","EASY"),
    ("MEDUIM","MEDUIM"),
    ("HARD","HARD")
]
POINTS = {
    "EASY":8,
    "MEDUIM":10,
    "HARD":12,
}

PENALTY = 300
class Contests(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    duration = models.DurationField()
    started = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True,blank=True)
    starred = models.BooleanField(default=False)
    key = models.TextField(blank=False,null=False)
    finished = models.BooleanField(default=False)

    def calculateTotalPoints(self):
        return sum([question.point for question in self.contest_question_set.all()])

    def __str__(self):
        return self.name
    
class Contest_Groups(models.Model):
    contest = models.ForeignKey(Contests,on_delete=models.CASCADE)
    group_name = models.CharField(max_length=40)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def calculateTime(self):
        totalTime = 0
        for submissions in self.contest_submissiosn_set.filter(solved=True):
            totalTime += submissions.submit_time

        return int(totalTime) 
    def calculatePenalty(self):
        return PENALTY * self.contest_submissiosn_set.filter(solved=False).count()
    
    def calculateTotalPoint(self):
        return sum([submission.question.point for submission in self.contest_submissiosn_set.filter(solved=True)])
    def __str__(self):
        return self.group_name

class Contestants(models.Model):
    name = models.CharField(max_length=40)
    group = models.ForeignKey(Contest_Groups,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    
class Contest_Question(models.Model):
    contest = models.ManyToManyField(Contests)
    title = models.CharField(max_length=40,unique=True)
    lvl = models.CharField(max_length=20,choices=QUESTION_LEVELS)
    point = models.IntegerField()
    description = models.TextField()
    time_limit = models.IntegerField(default=10)
    num_of_test_cases = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_solved(self):
        solved = self.Contest_submissiosn_set.filter(solved=True)
        return True if solved else False
    def __str__(self):
        return self.title
    

class Contest_submissiosn(models.Model):
    id = models.TextField(primary_key=True,unique=True)
    group = models.ForeignKey(Contest_Groups,on_delete=models.CASCADE)
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    lang = models.CharField(max_length=10)
    code = models.TextField()
    solved = models.BooleanField(default=False)
    status= models.CharField(max_length=30)
    submit_time = models.IntegerField()

    def __str__(self):
        return str(self.id)

