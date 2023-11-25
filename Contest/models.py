from django.db import models
from django.contrib.auth.models import User
QUESTION_LEVELS = [
    ("EASY","EASY"),
    ("MEDUIM","MEDUIM"),
    ("HARD","HARD")
]
class Contests(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    duration = models.DurationField()

    def __str__(self):
        return self.name
    
class Contest_Groups(models.Model):
    contest = models.ForeignKey(Contests,on_delete=models.CASCADE)
    group_name = models.CharField(max_length=40)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name

class Contestants(models.Model):
    name = models.CharField(max_length=40)
    group = models.ForeignKey(Contest_Groups,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    
class Contest_Question(models.Model):
    contest = models.ForeignKey(Contests,on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    lvl = models.CharField(max_length=20,choices=QUESTION_LEVELS)
    description = models.TextField()
    
    num_of_test_cases = models.IntegerField()
    def __str__(self):
        return self.title
    

class Contest_submissiosn(models.Model):
    group = models.ForeignKey(Contest_Groups,on_delete=models.CASCADE)
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    code = models.TextField()
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group.group_name)

class Contest_solutions(models.Model):
    group = models.ForeignKey(Contest_Groups,on_delete=models.CASCADE)
    submission = models.ForeignKey(Contest_submissiosn,on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    solved_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group.group_name)    
