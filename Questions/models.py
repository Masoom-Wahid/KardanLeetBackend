from Contest.models import Contests
from django.db import models
from Contest.models import Contest_Question
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible

    
class sample_test_cases(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    sample = models.CharField(max_length=70)
    answer = models.CharField(max_length=70)
    explanation  = models.CharField(max_length=70)
    def __str__(self):
        return str(self.question.title)

class Consttraints(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    consts = models.TextField()

    def __str__(self):
        return str(self.question.title)

class sample_test_cases_file(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    test_case_file =models.FileField(upload_to="temp_files")

    def __str__(self):
        return str(self.question.title)
