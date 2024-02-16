from secrets import token_urlsafe
from django.contrib.auth.models import User
from Contest.models import Contest_Groups
import random
import os
from django.conf import settings
from cryptography.fernet import Fernet

def generate_random_password():
    names = ["EH","HA","MW"]
    return f"{names[random.randint(0,2)]}_{token_urlsafe(6)}"


def read_file(key,
              contest_name,
              page,users_count,
              MAXIMUM_PER_PAGE_ALLOWED,
              all):
    """
    This Essentially Decrypts and Reads The Data from credentials.txt of the contest
    and then returns the users based on the page requested
    """
    # This is to Ensure that if the users are 64 and the page is 4
    # then the last index wouldnt be 80 but 64
    index = page*MAXIMUM_PER_PAGE_ALLOWED
    if index + MAXIMUM_PER_PAGE_ALLOWED > users_count:
        last_index = users_count
    else:
        last_index = index+MAXIMUM_PER_PAGE_ALLOWED 

    file_path = os.path.join(settings.BASE_DIR,"files","Contest","Credentials",f"{contest_name}__credentials.txt")
    with open(file_path,"rb") as file:
        previous_encrypted_data = file.read()


    """
    Used Arrays Because of thier Random Access Memroy Availability and better speed at reading for 
    pages
    """
    data = str(decrypt_file(key,previous_encrypted_data))[2:-1]
    contestants = []
    splitted = data.split(",")
    hash_table = {}
    for i in range(len(splitted) - 1 ):
        username,password = splitted[i].split("=")
        contestants.append([username,password])

    # if the user requires all of them we dont want to want to cut it by indexing them per page else the normal
    if all:
        for i in range(len(contestants)):
            username,password = contestants[i]
            hash_table[username] = password
    else:
        for i in range(index,last_index):
            username,password = contestants[i]
            hash_table[username] = password
    
    return hash_table


"""
Fernet Is 2 Way Encryption Algorithm.
It Requires The Key To Validate and Encrypt And Decrypt
"""
def encrypt_file(key,data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data

def decrypt_file(key,encrypted):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return decrypted


def write_credentials_file(key,contest_name,data,action):
    file_path = os.path.join(settings.BASE_DIR,"files","Contest","Credentials",f"{contest_name}__credentials.txt")
    # If The credentials.txt file is already created then we read and update the data based on that
    if action == "update":
        with open(file_path,"rb") as file:
            previous_encrypted_data = file.read()
        data_to_store = str(decrypt_file(key,previous_encrypted_data))[2:-1]
    else:
        data_to_store = ""

    
    for username,password in data.items():
        data_to_store += f"{username}={password},"

    encrypted_data = encrypt_file(key,data_to_store.encode())

    
    with open(file_path,"wb") as file:
        file.write(encrypted_data)



def generate_user_for_contest(amount,startFrom,contest_name,contest):
    passwords = {}
    for i in range(amount):
        user_name = f"{contest_name}__{i+startFrom}"
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
            group_name = f"{contest_name}__contestant__{i+startFrom}",
            contest = contest
        )
    if startFrom <= 1:
        write_credentials_file(contest.key,contest_name,passwords,"create")
    else:
        write_credentials_file(contest.key,contest_name,passwords,"update")
    return passwords