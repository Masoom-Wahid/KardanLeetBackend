# Competations

## Endpoints
* ### [GetQuestions](#createcontest-1)
* ### [Submissions](#submissions-1)
* ### [TestCode](#testcode-1)
* ### [Leaderboard](#leaderboard-1)

# GetQuestions
* ### [AllQuestions](#allquestions-1)
* ### [RetreiveQuestions](#retreivequestions-1)
* ## AllQuestions
* ### permissions : Authenticated Users
* ### Endpoint :
```
GET api/competition/
```
* ### returns the detail of a questions
<br>

* ## RetreiveQuestions
* ### permissions : Authenticated Users
* ### Endpoint :
```
GET api/competition/<question_id>
```
* ### returns all of the questions details , eg: testcases , constraints

<hr>

# Submissions
* ### [ShowSubmissions](#showsubmissions-1)
* ### [DetailOfSubmissions](#detailsubmissions)

* ## ShowSubmissions
* ### permissions : Authenticated Users
* ### Endpoint :
```
GET api/competition/<question_id>?submissions=True
```
* ### returns all the user's submissions for that particular questions
<br>

* ## DetailSubmissions
* ### permissions : Authenticated Users
* ### Endpoint :
```
GET api/competition/<question_id>?submissions=True&id=<submissions_id>
```
* ### returns the detail of that submissions with the code of it

<hr>

# TestCode
* ### This Endpoint Will Only Accept MULTIPART , NO JSON
* ### Before We Begin , here is the lanuages and their synonyms which we will use
```JSON
    "python":"python",
    "javascript":"javascript",
    "typescript":"typescript",
    "php":"php",
    "rust":"rust",
    "csharp":"csharp",
    "c":"c",
    "c++":"cpp",
    "java":"java"
```
<br>

* ### List of Response and there Meaning
```JSON
{
    "423":"THAT THE CONTEST HAS NOT STARTED YET or Has Finished,",
    "412":"the user has already solved the question",
    "404":"the question does not exist or the user does not have a group_instance(Contact Admin)",
    "406":{
        "NotAccpetable":"
            'THE ERRORS ARE ALWAYS RETURNED IN 'reason' key value pair' like this
            `
            reason:""
            `
            BELOW U CAN FIND THE LIST OF ERRORS
            WHICH WILL BE RETURNED AS VALUE FOR REASON
        ",
        "timeout":"it says that the code is taking longer the time_limit vairable",
        "InvalidAnswer":"The Output and Expected Output Are Not The Same",
        "Class Issues":"Only For Java And C# , this is when they make 2 classes(FORBIDDEN)",
        "Compilation Error":"Only For Compiled Lanuages such as ['java','c','cpp','typescript','rust','csharp']
        This means that there is a syntax error and that particular language could not be compiled into byte code",
        "Error":"This Probbably Happens Alot For Interperted Lanuages Since They Are Not Checked at Compile Time
        but rather at runTime. Any Syntax Error Should Be Reported Here",
        "Exception":"This is almost always the code or the server error , this should be treated like the status
        of 500 and is alwyas the problem of the server and not the code"
    }
}

```

* ### [RunCode](#runcode-1)
* ### [SubmitCode](#submitcode-1)
* ### [ManualRun](#manualrun-1)
<br>

* ## RunCode
* ### permissions : Authenticated Users
* ### Endpoint :
```
POST api/competition/
```
```JSON
    "lang":"python",
    "type":"run",
    "code":"Your Code File",
    "id":"questions_id"
```
* ### Runs The 2 First Testcases of the question

<br>

* ## SubmitCode
* ### permissions : Authenticated Users
* ### Endpoint :
```
POST api/competition/
```
```JSON
    "lang":"python",
    "type":"submit",
    "code":"Your Code File",
    "id":"questions_id"
```
* ### Runs All the testcases
* ### Failing The Questions Here Will Cause The User A 5 minute penalty

<br>

* ## ManualRun
* ### permissions : Authenticated Users
* ### Endpoint :
```
POST api/competition/
```
```JSON
    "lang":"python",
    "type":"manual",
    "code":"Your Code File",
    "id":"questions_id",
    "manual_testcase":"2\n4\n"  \\ "\n" indicates the end of the line , this should not be a file , just plain text
```
* ### Runs The Submitted File with the given input


# LeaderBoard
* ### permissions : Admin
* ### Endpoint :
```
ws:<Domain>/leaderboard/?token=${accessToken}
```
* ### for local testing eg:
```
ws://127.0.0.1:8000/leaderboard/?token=${accessToken}
```


