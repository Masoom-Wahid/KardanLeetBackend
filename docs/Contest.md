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



# ListContest
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/
```
* #### Returns all the contests
<hr>

# RetreiveContest
* #### [listgroups](#listgroups-1)
* #### [listresults](#listresults-1)
<br>

* ### listgroups
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/<id>
```
* #### Returns the groups in that contest
<br>

* ### listresults
* #### permissions : Admin
* #### Endpoint : 
```
GET api/contest/<id>?results=True
```
* #### Returns the results of that contest

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
```
POST api/contest/groups/
```
```JSON
    "name":"Fall 2023"
```

* #### returns all the contest group in the given contest

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
    "action":"do_start"
```
* ### it stars the contest
* ### NOTE : You Can Only Have One Starred Contest at a time
<br>

```JSON
    "name":"Fall 2023",
    "action":"undo_start"
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