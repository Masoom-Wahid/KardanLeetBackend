from secrets import token_urlsafe
from django.contrib.auth.models import User
from Contest.models import Contest_Groups
import random

def generate_random_password():
    names = ["EH","HA","MW"]
    return f"{names[random.randint(0,2)]}_{token_urlsafe(12)}"

def generate_user_for_contest(amount,startFrom,contest_name,contest):
    passwords = {}
    for i in range(amount):
        user_name = f"{contest_name}__{i+1+startFrom}"
        password = generate_random_password()
        passwords[user_name] = password
        instance = User.objects.create(
            username = user_name,
            email = f"{user_name}@email.com",
        )
        instance.set_password(password)
        instance.is_active = True
        instance.save()
        Contest_Groups.objects.create(
            user = instance,
            group_name = f"contestant__{i}",
            contest = contest
        )
    return passwords