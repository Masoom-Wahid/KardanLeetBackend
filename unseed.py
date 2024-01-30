"""
	This Should Be Used To Delete The Data Created From 
	Seed.py.
"""


import django
import random
from datetime import timedelta
from django.utils import timezone
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"]="KardanLeet.settings"

django.setup()

from Contest.models import Contests,Contest_Groups,Contest_Question
from Conte.tasks import scheduler

CONTEST_NAME = "Winter2023"
QUESTIONS = ["FactorialOfANumber","FindThePalindrome","TwoSum"]

print("Deleting the data created by seed.py")

try:
	contest_instance = Contests.objects.get(name=CONTEST_NAME)
except Contests.DoesNotExist as e:
	print(e)
	print("You Have Already Deleted The Contest Instance")
	sys.exit()


try:
    scheduler.remove_job("Contest_Listener")
except:
    print("Listener Already Removed")

contest_instance.delete()

for group in Contest_Groups.objects.filter(contest=contest_instance):
	group.user.delete()
	group.delete()

for question in QUESTIONS:
	question_instance = Contest_Question.objects.get(title=question)
	question_instance.delete()

print("Deleting Completed")