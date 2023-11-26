from secrets import token_urlsafe
from django.contrib.auth.models import User
from Contest.models import Contest_Groups
def generate_random_password():
    return token_urlsafe(12)

def generate_user_for_contest(amount,contest_name,contest):
    passwords = {}
    for i in range(1,amount+1):
        user_name = f"{contest_name}__{i}"
        password = generate_random_password()
        passwords[user_name] = password
        instance = User.objects.create(
            username = user_name,
            email = f"{user_name}@email.com",
            password =password
        )
        Contest_Groups.objects.create(
            user = instance,
            group_name = f"contestant__{i}",
            contest = contest
        )
    return passwords