# Questions
<hr>

## Endpoints
* ### [ListQuestion](#list-questions)
* ### [CreateQuestions](#create-questions)
* ### [test_cases](#testcases)
* ### [question_files](#questionsfiles)
<hr>

# List Questions
### Permissions : Admin
### Endpoint:
```
GET api/questions?name=<contestname>
```
#### returns all the questions in the given contest
<hr>

# Create Questions
* #### Permissions : Admin
* #### Endpoint:
```
POST api/questions/
```
* #### requires title,lvl(HARD,MEDUIM,EASY),point,time_limit,num_of_test_cases,description
* #### time_limit is not mandatory , if not given it will be defaulted to 10
```JSON
    "title":"Factorial",
    "lvl":"EASY",
    "point":"10",
    "time_limit":"8",
    "num_of_test_cases":"12",
    "description":"Find The Factorial Of The Given Number",
```
* #### num_of_test_cases if important since it shows the maximum number of testcases which will be given
<hr>

# TestCases
* #### !!! This Is The Testcases which are shown under the description and are just for explanation
* #### Permissions : Admin
* #### Endpoint: 
```
POST api/questions/testCases/
```
* #### requires -> id(question_id),sample,answer,example
```JSON
    "id":"1",
    "sample":"",
    "answer":"",
    "explanation":"",
    "
```
<hr>

# QuestionsFiles
* #### !!! These are the files which the user will be judged from
* #### Permissions : Admin
* #### Endpoint: 
```
POST api/questions/files/
```
* #### requires -> id(question_id),files
* #### it should multipart not JSON
<br>

```JSON
    "id":"1",
    "files":"input1.txt",
    "files":"output1.txt",
    "files":"input2.txt",
    "files":"output2.txt"
    "
```

* #### based on the num_of_test_cases given when giving the question all the input and output should exist , so if given 3 then there should input1,input2,input3 and output1,output2,output2 -> naming them like this are mandatory
<br>

* #### Endpoint : if u want to see the num of testcases of a question 
```
GET api/questions/files?contest=<contest_name>&question=<question_id>
```
* #### this just returns a number which is the num of testCases
<br>

* #### Endpoint : if u want to see the data of a file in the question's testcases
```
GET api/questions/files?contest=<contest_name>&question=<question_id>&id=<testfile_id>
```

* #### id should be smth like this : if u want to see input1 then id is input1 so it is the naming convention from before

<br>

* #### Permissions : Admin
* #### Endpoint: 
```
PUT api/questions/files/
```
* #### requires -> id,file,contest(contest_name),question(question_id)
* #### id is input1,input2 , which file of the question u want to change 
* #### it should multipart not JSON
<br>

```JSON
    "id":"input",
    "file":"input1.txt",
    "contest":"",
    "question":"",
```

* #### it changes the said file to that given file

## Continue [here](./Contest.md)

