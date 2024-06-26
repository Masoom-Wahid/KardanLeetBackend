# Questions
<div class="border-break"></div>

## Endpoints
* ### [ListQuestion](#list-questions)
* ### [CreateQuestions](#create-questions)
* ### [DeleteQuestions](#delete-questions)
* ### [UpdateQuestion](#updating-questions)
* ### [SampleTestCases](#sampletestcases-1)
* ### [Constraints](#constraints-1)
* ### [question_files](#questionsfiles)
* ### [search](#search-questions-1)

<div class="break"></div>

# <span class="text">List Questions<span>
### Permissions : Admin
### Endpoint:
```
GET api/questions?name=<contestname>&page=2
```
#### name is not mandatory , if not given it will return all the questions
#### page is not mandatory , if not given it will be set to 1
#### returns all the questions in the given contest
<div class="break"></div>

 
# <span class="text">Create Questions<span>
* #### Permissions : Admin
* #### Endpoint:
```
POST api/questions/
```
* #### time_limit is not mandatory , if not given it will be defaulted to 10
```JSON
    "name":"Autumn2022",
    "title":"Factorial",
    "lvl":"EASY",
    "point":"10",
    "time_limit":"8",
    "num_of_test_cases":"12",
    "description":"Find The Factorial Of The Given Number",
```
* #### num_of_test_cases is important since it shows the maximum number of testcases which will be given
* #### for adding a testcase files see [here](#questionsfiles) , for constraints [here](#constraints-1) , for samples [here](#sampletestcases-1)
<div class="break"></div>

# <span class="text">Delete Questions<span>
* #### Permissions : Admin
* #### Endpoint:
```
DEL api/questions/<id>
```
* #### it will also delete all of the TESTCASE files if there is any
<div class="break"></div>

# <span class="text">Updating Questions<span>
* #### Permissions : Admin
* #### Endpoint: 
```
POST api/questions/<id>
```
```JSON
	"contest":"Autumn_2022",
	"title":"thisSum",
	"lvl":"EASY",
	"point":"20",
	"time_limit":"10",
	"description":"jama ko",
	"num_of_test_cases":"3"
```
<div class="break"></div>

# <span class="text">Search Questions<span>
### Permissions : Admin
### Endpoint:
```
GET api/questions/search/?title=<title>
```
#### filter the question based on the given title
<div class="break"></div>

# <span class="text">SampleTestCases<span>
* #### !!! This Is The Testcases which are shown under the description and are just for explanation
* #### Permissions : Admin
* #### ---FOR CREATING----
* #### Endpoint: 
```
POST api/questions/samples/
```
```JSON
    "question":"1",
    "sample":"",
    "answer":"",
    "explanation":"",

```

* #### ---FOR UPDATING----
* #### Endpoint: 
```
PUT api/questions/samples/<id>
```
```JSON
    "question":"1",
    "sample":"",
    "answer":"",
    "explanation":"",

```
* #### ---FOR DELETING----
* #### Endpoint: 
```
DEL api/questions/samples/<id>
```

<div class="break"></div>

# <span class="text">Constraints<span>
* #### permissions : Admin
* #### Note :All Constraints Should be given in one filed
* #### ---FOR CREATING----
* #### Endpoint: 
```
POST api/questions/constraints/
```
```JSON
    "question":"1",
    "consts":"n<=10\nk<2**10"

```

* #### ---FOR UPDATING----
* #### Endpoint: 
```
PUT api/questions/constraints/<id>
```
```JSON
    "question":"1",
    "consts":"n<=10\nk<2**10

```
* #### ---FOR DELETING----
* #### Endpoint: 
```
DEL api/questions/constraints/<id>
```
<div class="break"></div>

# <span class="text">QuestionsFiles<span>
* #### !!! These are the files which the user will be judged from
* #### Permissions : Admin
* #### Endpoint: 
```
POST api/questions/testcases/
```
* #### requires -> id(question_id),input and output
<br>

```JSON
    {
        "id":"1",
        "input":"3\n3\n4\n5\n",
        "output":"6\n24\n120"
    }
```

* ### it will return 400 if the testcases are already complete
<br>
<div class="break"></div>

* #### Endpoint : if u want to see the num of testcases of a question and if the testcases exists 
* #### and number of avaialable testcases
```
GET api/questions/testcases?question=<question_id>
```
* #### this just returns a number which is the num of testCases
<div class="break"></div>

* #### Endpoint : if u want to see the data of a file in the question's testcases
```
GET api/questions/testcases?question=<question_id>&id=<testfile_id>
```

* #### id should be smth like this : if u want to see input1 and output1 then id is 1 so it is the naming convention from before but just the number

<div class="break"></div>

* #### Permissions : Admin
* #### Endpoint: 
```
PUT api/questions/files/
```
* #### id is input1,input2 , which file of the question u want to change 
* #### it should MULTIPART not JSON
<br>

```JSON
    {
        "id":"1",
        "question":"1",
        "input":"4\n3\n3\n4\n5\n",
        "output":"6\n6\n24\n120"
    }
```

* #### it changes the said file to that given file

## Continue [here](./Contest.md)

