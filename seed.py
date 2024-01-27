"""
Use This For Only Creating Fake Data,Or Mainly Debugging Purposes.
"""
from seed.seedFunctions import *
import sys


"""ACCESS_TOKEN FOR CREATING DATA"""
ACCESS_TOKEN = None
"""EMAIL AND PASSWORD FROM THE INPUT"""
ADMIN_USERNAME = None
ADMIN_PASSWORD = None
"""ID OF THE CREATED CONTEST"""
CONTEST_ID = None




if __name__ == "__main__":
    ADMIN_USERNAME = input("Your Username (Superuser Account Username): ") or None
    ADMIN_PASSWORD = input("Password: ") or None
    if ADMIN_USERNAME and ADMIN_PASSWORD:
        """
            Authenticate The User
        """
        didSuccessFullAuth ,ACCESS_TOKEN = getAccessToken(ADMIN_USERNAME,ADMIN_PASSWORD)
        if not didSuccessFullAuth:
            print(f"""{TerminalColors.FAIL}Invalid Email or Password{TerminalColors.ENDC}""")
        else:
            print(f"""{TerminalColors.OKGREEN}STARTING THE SEED........{TerminalColors.ENDC}""")

        """
            CREATEING A CONTEST
        """
        print(f"""{TerminalColors.OKBLUE}CREATING A CONTEST........{TerminalColors.ENDC}""")
        didSuccessFullContestCreation,CONTEST_ID = createContest(ACCESS_TOKEN)
        if didSuccessFullContestCreation:
            print(f"""{TerminalColors.OKGREEN}Contest Created........{TerminalColors.ENDC}""")
        else:
            print(f"""{TerminalColors.FAIL}Failed Creating The Contest, Maybe A Contest With The Given Name Already Exists? {TerminalColors.ENDC}""")
            sys.exit()


        """
            CREATING THE QUESTIONS
        """
        print(f"""{TerminalColors.OKBLUE}CREATING Questions........{TerminalColors.ENDC}""")
        didSuccessFullQuestionCreation = createQuestions(ACCESS_TOKEN)
        if didSuccessFullQuestionCreation:
            print(f"""{TerminalColors.OKBLUE}Questions Created........{TerminalColors.ENDC}""")

        """
            ASSIGNING THE QUESTIONS THE CREATED CONTEST
        """
        #assign the questions
        print(f"""{TerminalColors.OKBLUE}Assigning The Questions To The Contest........{TerminalColors.ENDC}""")
        didSuccessFullQuestionAssignment = assignQuestions(ACCESS_TOKEN)         
        if didSuccessFullQuestionAssignment:   
            print(f"""{TerminalColors.OKBLUE}Questions Created........{TerminalColors.ENDC}""")
        else:
            print(f"""{TerminalColors.FAIL}Failed Assigning The Questions{TerminalColors.ENDC}""")
            sys.exit()
        """
            CREATING 2 CONTEST GROUPS
        """
        print(f"""{TerminalColors.OKBLUE}Creating 2 The Contest Groups For The Contest........{TerminalColors.ENDC}""")
        didSuccessFullQuestionAssignment,data = createContestGroups(ACCESS_TOKEN,CONTEST_ID)         
        if didSuccessFullQuestionAssignment:   
            print(f"""{TerminalColors.OKBLUE}Contest Groups Created........{TerminalColors.ENDC}""")
            print(f"""{TerminalColors.BOLD}UserName And Password Are:\n{
                data}{TerminalColors.ENDC}""")
        else:
            print(f"""{TerminalColors.FAIL}Failed Creating The Conetst Groups{TerminalColors.ENDC}""")
            sys.exit()


        """
            STARRING AND STARTING THE CONTEST
        """        
        print(f"""{TerminalColors.OKBLUE}STARRING AND STARTING THE CONTEST........{TerminalColors.ENDC}""")
        didStarrTheContest = starTheContest(ACCESS_TOKEN)
        if not didStarrTheContest:
            print(f"""{TerminalColors.FAIL}Failed Starring The Conetst {TerminalColors.ENDC}""")
            sys.exit()
        didStartTheContest = startTheContest(ACCESS_TOKEN) 
        if not didStarrTheContest:
            print(f"""{TerminalColors.FAIL}Failed Starting The Conetst {TerminalColors.ENDC}""")
            sys.exit()

        print(f"""{TerminalColors.OKBLUE}CONTEST STARRED AND STARTED........{TerminalColors.ENDC}""")
        print(f"""{TerminalColors.OKBLUE}SEEDING FINISHED........{TerminalColors.ENDC}""") 

    else:
        print(f"""{TerminalColors.FAIL}Make To Sure To Not Pass Empty As Email or Password{TerminalColors.ENDC}""")


