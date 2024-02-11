import requests
import json
import threading
import time
import sys
from .seedData import CONTEST_NAME,SEED_DATA
from .urlEndpoints import UrlEndpoints
from .TerminalColors import TerminalColors
# Function For Getting The Headers For Every Request
QUESTION_IDS = {}

def getHeaders(accessToken=None) -> dict:
    if accessToken :return  {
        "Content-Type": "application/json",
        "Authorization" : f"Bearer {accessToken}"
    } 
    else: return {
        "Content-Type": "application/json",
    }
        
def print_loading(event, message=None):
    animation = "|/-\\"

    while not event.is_set():
        if message is not None:
            sys.stdout.write("\r" + message)
            sys.stdout.flush()

        for char in animation:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)

        sys.stdout.write(" " * len(animation))
        sys.stdout.flush()

    

def createPOSTRequest(url,data,accessToken=None,require_load_animation=True) -> [bool,str]:
    if not require_load_animation:
        response = requests.post(
        url,
        data=json.dumps(data),
        headers=getHeaders(accessToken))

        if response.status_code == 204:
            return True,""
        if response.status_code == 200 or response.status_code == 201:
            return True,response.json()
        else:
            return False,""
    else:
        event = threading.Event()
        threading.Thread(target=print_loading, args=(event, "Loading......")).start()
        response = requests.post(
            url,
            data=json.dumps(data),
            headers=getHeaders(accessToken))
        
        event.set()
        time.sleep(0.1)
        print("\r" + " " * 50, end="")
        print()
        if response.status_code == 204:
            return True,""
        if response.status_code == 200 or response.status_code == 201:
            return True,response.json()
        else:
            return False,""


def getAccessToken(username,password) -> [bool, str]:
    response,data = createPOSTRequest(
                                    UrlEndpoints["auth"],
                                      {"username":username,
                                       "password":password
                                       })
    if response:
        return True,data["access"]
    else:
        return False,""


def createContest(accessToken) -> [bool,str]:
    response,data = createPOSTRequest(UrlEndpoints["createContest"],{
        "name":SEED_DATA["contestDetail"]["contestName"],
        "duration":SEED_DATA["contestDetail"]["duration"]
    },
    accessToken)
    if response:
        return True,data["id"]
    else:
        return False,""

def createQuestionInstance(name,data,accessToken) -> [bool,str]:
    data['title']=name
    response,data = createPOSTRequest(
        UrlEndpoints['createQuestions'],
        data,
        accessToken
    )
    if response:
        return True,data["id"]
    else:
        return False,""

def createTestCases(id,data,accessToken):
    data['id']=id
    response,data = createPOSTRequest(
        UrlEndpoints['createTestCases'],
        data,
        accessToken,
        require_load_animation=False
    )
    if response:
        pass
    else:
        return False
        
    return True

def createSamples(id,data,accessToken):
    data['question'] = id
    response,data = createPOSTRequest(
        UrlEndpoints['createSamples'],
        data,
        accessToken,
        require_load_animation=False
    )
    if response:
        return True
    else:
        return False

def createConstraints(id,data,accessToken):
    data['question'] = id
    response,data = createPOSTRequest(
        UrlEndpoints['createConstraints'],
        data,
        accessToken,
        require_load_animation=False
    )
    if response:
        return True
    else:
        return False

def createQuestions(ACCESS_TOKEN) -> [bool,str]:
    for key,value in SEED_DATA["questionsDetail"].items():
        response,id = createQuestionInstance(key,value["data"],ACCESS_TOKEN)
        print(f"""{TerminalColors.OKGREEN}Question Created........{TerminalColors.ENDC}""")
        QUESTION_IDS[key] = id
        if response:
            for i in range(int(value["data"]['num_of_test_cases'])):
                testCaseResponse = createTestCases(id,
                                                    value['testcases'],
                                                    ACCESS_TOKEN
                                                                )
                if not testCaseResponse:
                    print(f"""{TerminalColors.FAIL}Failed Creating The TestCases {TerminalColors.ENDC}""")
                    sys.exit()
                
            sampleTestCaseResponse = createSamples(id,
                                                value['samples'],
                                                ACCESS_TOKEN
                                                )    
            if not sampleTestCaseResponse:
                print(f"""{TerminalColors.FAIL}Failed Creating The Samples {TerminalColors.ENDC}""")
                sys.exit()

            sampleTestCaseResponse = createConstraints(id,
                                                value['consts'],
                                                ACCESS_TOKEN
                                                )    
            if not sampleTestCaseResponse:
                print(f"""{TerminalColors.FAIL}Failed Creating The Constraints {TerminalColors.ENDC}""")
                sys.exit()
    return True


def assignQuestions(ACCESS_TOKEN) -> bool:  
    ids = ",".join([str(value) for key,value in QUESTION_IDS.items()])
    data = {
        "name":CONTEST_NAME,
        "ids":ids
    }
    response,data = createPOSTRequest(
        UrlEndpoints['assignQuestions'],
        data,
        ACCESS_TOKEN
    )
    if response:
        return True
    else:
        return False
            
        
def createContestGroups(ACCESS_TOKEN,CONTEST_ID) -> bool:
    data = {
        "type":"contest",
        "amount":"2",
        "contest_id":CONTEST_ID
    }
    response,data = createPOSTRequest(
        UrlEndpoints['createGroup'],
        data,
        ACCESS_TOKEN
    )
    if response:
        return True,data
    else:
        return False,""

def starTheContest(ACCESS_TOKEN) -> bool:
    data = {
        "name":CONTEST_NAME,
        "action":"do_star",
    }
    response,data = createPOSTRequest(
        UrlEndpoints['actions'],
        data,
        ACCESS_TOKEN
    )
    if response:
        return True
    else:
        return False,""

def startTheContest(ACCESS_TOKEN) -> bool:
    data = {
        "name":CONTEST_NAME,
        "action":"do_start",
    }
    response,data = createPOSTRequest(
        UrlEndpoints['actions'],
        data,
        ACCESS_TOKEN
    )
    if response:
        return True
    else:
        return False,""