# Contest

## Endpoints
* ### [ListContest](#)
* ### [RetreiveContest]()
* ### [CreateContest](#createcontest-1)
* ### [DeleteContest](#deletecontest-1)
* ### [UpdateContest](#updatecontest-1)
* ### [ContestGroups](#contestgroups-1)
* ### [Contestants](#contestants-1)
* ### [Actions](#actions-1)
* ### [Stats](#stats)
* ### [setQuestions](#setquestions-1)



# ListContest
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/
```
* #### Returns all the contests
<hr>

# RetreiveContest
* #### [listgroups](#detail-1)
* #### [listgroups](#listgroups-1)
* #### [listresults](#listresults-1)
* #### [cleanCache](#listresults-1)
<br>

* ### Detail
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/<id>
```
* #### Returns the detail of that contest
<br>
* ### Groups
* #### permissions : Admin
* #### Endpoint : 

```
GET api/contest/<id>?groups=True<id>
```
* #### Returns the Groups of that contest
<br>


* ### listresults
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/<id>?results=True
```
* #### Returns the results of that contest
<br>


* ### cleanCache
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/<id>?clean_cache=True
```
* #### used for cleaning the leaderboard cache for contest

<hr>



# CreateContest
* #### permissions : Admin
* #### Endpoint : 
```
POST api/contest/
```
```JSON
    "name":"Fall 2023",
    "duration":"00:00:10"
```
* #### The Name Should Be Unique
<hr>

# UpdateContest
* #### permissions : Admin
* #### Endpoint : 
```
POST api/contest/<id>
```
```JSON
	"name":"Autumn_2024",
	"duration":"00:00:10"
```
* #### The Name Should Be Unique
<hr>

# DeleteContest
* #### permissions : Admin
* #### Endpoint : 
```
 api/contest/<id>
```
<hr>

# ContestGroups
* #### permissions : Admin
* #### Endpoint : 

* ### [ListGroups](#list-groups)
* ### [ListSubmissions](#list-submissions)
* ### [SubmissionDetail]


## LIST GROUPS
```
GET api/contest/groups?contest=<contest_name>&page=<page_number>
```
* ####  by default page is set to 1 , but contest is mandatory
* #### the response should be smth like this
* #### maximum of 6 groups allowed per pages
```JSON
{
	"avaialabe_pages": 11,
	"data": [
		{
			"id": 107,
			"group_name": "contestant__19",
			"contest": 9,
			"user": 111
		},
		{
			"id": 108,
			"group_name": "contestant__20",
			"contest": 9,
			"user": 112
		},
		{
			"id": 109,
			"group_name": "contestant__21",
			"contest": 9,
			"user": 113
		},
		{
			"id": 110,
			"group_name": "contestant__22",
			"contest": 9,
			"user": 114
		},
		{
			"id": 111,
			"group_name": "contestant__23",
			"contest": 9,
			"user": 115
		},
		{
			"id": 112,
			"group_name": "contestant__24",
			"contest": 9,
			"user": 116
		}
	]
}
```

* #### returns all the contest group in the given contest according to their page number

## LIST SUBMISSIONS
### [FILTERS](#filters)
```
GET api/contest/groups?id=<group_id>&page=<page_number>
```
* ####  by default page is set to 1 , but id is mandatory
* #### the response should be smth like this
```JSON
{
	"avaialabe_pages": 3,
	"submissions_count": 14,
	"data": [
		{
			"id": "dzzrtKaEtHQ8mDy-AXgZ8w",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 282
		},
		{
			"id": "UQGpUINreRl12YGWbwaMhw",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 281
		},
		{
			"id": "kIgtue6mK2kOXKyzWgJTyA",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 278
		},
		{
			"id": "8vDPVv2PXsDc0bZ-D8FJJg",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 276
		},
		{
			"id": "2poq6wx2hsrxbjav31FukQ",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 273
		},
		{
			"id": "tsGlLvkJpWlEf3uEZrUYiw",
			"code": "",
			"group": "contestant__1",
			"question": "Palindrome",
			"lang": "python",
			"solved": true,
			"status": "Solved",
			"submit_time": 271
		}
	]
}
```
* #### maximum of 6 submissions allowed per pages
### FILTERS
* #### solved -> "True" or "False"
* #### time -> "earliest" or "oldest"
* #### lang -> should be the lanuages listed in [here](./Competetion.md#testcode-1)
* #### An Example EndPoint is Smth Like This
```JSON
GET api/contest/groups/?id=89&solved=True&lang=python&page=2&time=earliest
```
* #### Note that filters are not mandatory and nor is page, the page is set to 1 by default 
* #### only id is mandatoy here
<hr>

## SUBMISSION DETAIL
```
GET api/contest/groups/?submission_id=tKIjSuOXwiYRLGDDy3lZGg
```
### It returns the detail of that submission
### The Response should look smth like this
```JSON
{
	"id": "tKIjSuOXwiYRLGDDy3lZGg",
	"code": "# Do Not Print Unnecesary Stuff and let the input function to \n# empty or '' ie: input()\ntestcases = int(input())\nfor _ in range(testcases):\n    word = input()\n    # print(f\"word is {word} and revrse is {word[::-1]}\")\n    if word == word[::-1]:\n        print(\"True\")\n    else:\n        print(\"False\")",
	"group": "contestant__1",
	"question": "Palindrome",
	"lang": "python",
	"solved": true,
	"status": "Solved",
	"submit_time": 240
}
```

<hr>

# Contestants
* #### [GetContestant](#getcontestant-1)
* #### [CreateContestant](#createcontestant-1)
* #### [DeleteContestant](#deletecontest-1)
<br>

* ### GetContestant
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/contestants?id=<group_id>
``` 
* ### returns all the contestants in that particular group
<br>

* ### CreateContestant
* #### permissions : Admin
* #### Endpoint : 
```
POST api/contest/contestants/
``` 
```JSON
    "id":"10", // by id we mean the group id
    "name":"Ahmad"
```
<br>

* ### DeleteContestant
* #### permissions : Admin
* #### Endpoint : 
```
DEL api/contest/contestants?id=<contestant_id>
``` 
<hr>

# setQuestions
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/setQuestions/
```

```JSON
	{
	"name":"Autumn2022",
	"ids":"1,2,3,4,"
}
```

* #### ids is the id of question u want the contest u want to connect to and that end ',' is mandatory
<hr>

# Stats
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/stats/?contest=<contest_name>
```
* ### "contest" is not mandatory , if not given it will the return the stats of the "starred" contest
* ### if given , it will return the result of that given contest

* ### The Response Should Be Smth Like This
```JSON
{
	"previous_contest_groups": [
		{
			"contest__name": "Autumn2024",
			"group_count": 4
		}
	],
	"current_contest" : {
	"Active Contestants":10,
	"Number of Challenges":1,
	"Correct Answers":23,
	"Incorrect Answers":33,
	}
}
```

<hr>

# Actions
* ### By actions we mean starting,resetting,starring,finishing the contest
* #### permissions : Admin
* #### Endpoint : 
```
POST api/contest/actions/
```

```JSON
    "name":"Fall 2023",
    "action":"do_start"
```
* ### Here is how it works , u prefix the thing u want to do with do or undo and the followed by a _ and then that the name of action

* ### List of actions You Can Do
<br>

```JSON
    "name":"Fall 2023",
    "action":"do_start"
```
* ### This starts the starred contest and also puts a worker or background scheduler to finish the timer of the contest based on the time given for the contest when creating it 
<br>

```JSON
    "name":"Fall 2023",
    "action":"undo_start"
```
* ### This Just Pauses the Worker and makes the start boolean untrue
<br>

```JSON
    "name":"Fall 2023",
    "action":"resume_start"
```
* ### it resumes the worker the Worker and starts the contst again from where we left off
<br>

```JSON
    "name":"Fall 2023",
    "action":"do_reset"
```
* ### removes the worker and the boolean start will be False
<br>

```JSON
    "name":"Fall 2023",
    "action":"do_star"
```
* ### it stars the contest
* ### NOTE : You Can Only Have One Starred Contest at a time
<br>

```JSON
    "name":"Fall 2023",
    "action":"undo_star"
```
* it unstars the contest
<br>

```JSON
    "name":"Fall 2023",
    "action":"do_finish"
```
* ### if for some reason the worker fails then this is a manual way to finish the contest
<br>

```JSON
    "name":"Fall 2023",
    "action":"undo_finish"
```
* ### it sets the Finish boolean to false

## Continue [here](./Competetion.md)