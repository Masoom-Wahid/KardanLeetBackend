from Contest.models import Contests
from django.db import models
from Contest.models import Contest_Question
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible

# @deconstructible
# class RenameStorage(FileSystemStorage):
#     def __init__(self, instance):
#         self.instance = instance
#     def _save(self, name, content):
#         new_name = f"{self.instance.question.contest.name}__{self.instance.question.name}__{name}"
#         return super()._save(new_name, content)

# def files_upload_path(instance,filename):
#     path = f"{instance.question.contest.name}/{instance.question.title}/"
#     return f"contest/{path}"

class sample_test_cases(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    sample = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return str(self.question.title)

class sample_test_cases_file(models.Model):
    question = models.ForeignKey(Contest_Question,on_delete=models.CASCADE)
    test_case_file =models.FileField(upload_to="temp_files")

    def __str__(self):
        return str(self.question.title)