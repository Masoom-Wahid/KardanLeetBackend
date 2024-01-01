# *API Documentation*

## *Questions*

### *Endpoints*

### List Questions

- *Permissions:* Admin
- *Endpoint:* *GET api/questions?name=<contestname>*
- *Description:* Returns all the questions in the given contest.

### Create Questions

- *Permissions:* Admin
- *Endpoint:* *POST api/questions/*
- *Description:* Creates a new question.
- *Parameters:*
    - *title*: Question title.
    - *lvl*: Difficulty level (HARD, MEDIUM, EASY).
    - *point*: Points for the question.
    - *time_limit*: Time limit for the question. Default is 10 if not provided.
    - *num_of_test_cases*: Number of test cases.
    - *description*: Description of the question.
- *Example Request Body:*
    
    json
    jsonCopy code
    {
      "title": "Factorial",
      "lvl": "EASY",
      "point": "10",
      "time_limit": "8",
      "num_of_test_cases": "12",
      "description": "Find The Factorial Of The Given Number"
    }
    
    
    

### *Test Cases*

- *Permissions:* Admin
- *Endpoint:* *POST api/questions/testCases/*
- *Description:* Add test cases to a question.
- *Parameters:*
    - *id*: Question ID.
    - *sample*: Sample data.
    - *answer*: Answer data.
    - *explanation*: Explanation of the test case.
- *Example Request Body:*
    
    json
    jsonCopy code
    {
      "id": "1",
      "sample": "",
      "answer": "",
      "explanation": ""
    }
    
    
    

### *Questions Files*

- *Permissions:* Admin
- *Endpoint:* *POST api/questions/files/*
- *Description:* Upload files for question test cases. Must be multipart, not JSON.
- *Parameters:*
    - *id*: Question ID.
    - *files*: Files for the question.
- *Notes:* Based on *num_of_test_cases* given in the question, corresponding input and output files should exist (e.g., input1, input2, output1, output2).
- *Example Request Body:*
    
    
    multipartCopy code
    id: 1
    files: input1.txt
    files: output1.txt
    files: input2.txt
    files: output2.txt
    
    
    

### View Number of Test Cases

- *Endpoint:* *GET api/questions/files?contest=<contest_name>&question=<question_id>*
- *Description:* Returns the number of test cases for a question.

### View Data of a File in Test Cases

- *Endpoint:* *GET api/questions/files?contest=<contest_name>&question=<question_id>&id=<testfile_id>*
- *Description:* Returns the data of a specific test file.

### Update Test File

- *Permissions:* Admin
- *Endpoint:* *PUT api/questions/files/*
- *Description:* Updates a specific test file for a question.
- *Parameters:*
    - *id*: File identifier (e.g., input1, input2).
    - *file*: The file to upload.
    - *contest*: Contest name.
    - *question*: Question ID.
- *Example Request Body:*