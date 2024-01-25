from django.db import models
from Contest.models import Contest_Question

    
class SampleTestCasesExample(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    sample = models.CharField(max_length=70)
    answer = models.CharField(max_length=70)
    explanation  = models.CharField(max_length=70)
    def __str__(self):
        return str(self.question.title)

class Constraints(models.Model):
    question = models.OneToOneField(Contest_Question,on_delete=models.CASCADE)
    consts = models.TextField()

    def __str__(self):
        return str(self.question.title)


class SampleTestCases(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    testCase = models.TextField()

    def __str__(self):
        return str(f"{self.question.title} -- {self.name} ")
