# Auth
<hr>

## Endpoints
* ### [Creating Admins](#creating-admins)
* ### [Creating ContestGroups](#contest-group-and-user-creation)
* ### [Creating Alias For ContestGroups](#creating-alias)
* ### [getCredentials](#get-credentials)

<hr>

# Creating Admins
* #### Permissions : Admin
* ##### EndPoint:
```shell
POST auth/users/
```
<br>

* #### requires : type -> normal,username,password
```JSON
    {
        "type":"normal",
        "username":"admin",
        "email":"email@gmail.com",
        "password":"password"
    }
```
<hr>

# Contest Group And User Creation
* #### Permissions : Admin
* ##### EndPoint:
```shell
POST auth/users/
```
<br>

* #### requires : type -> contest,amount,contest_id
```JSON
    {
        "type":"contest",
        "amount":"20",
        "contest_id":"1"
    }
```
* ##### Note: This Makes Contestants From Where The Contest has , so if contest has 20 Groups it will start naming them from 21 and so on ...
<hr>

# Creating Alias
* #### Permissions : Admin
* ##### EndPoint:
```shell
POST auth/users/alias/
```
<br>

* #### requires : username,alias
```JSON
    {
        "username":"username",
        "alias":"Constructors",
    }
```
* ##### Note: If There Is No Alias For The Given Group it will show the random generated one from when the group was created
<hr>


# GET CREDENTIALS
* #### Permissions : Admin
* ##### EndPoint:
```shell
GET auth/users/getcredentials?contest=Autumn2023&page=4
```
<br>

* #### NOTE :  You Can Also Get ALl of The Crednetials using this url
```shell
GET auth/users/getcredentials?contest=Autumn2023&all=True
```
* #### This Will Return all the users of that contest
* #### requires : contest and page
* #### contest is mandatory but page is set default to 1
* #### it should return smth like this
```JSON
    {
        "avaialable_pages": "4",
        "current_page": 4,
        "result": {
            "Autumn2023__61": "HA_BAjXZghi",
            "Autumn2023__62": "MW_1xCeX9x2",
            "Autumn2023__63": "EH_oaVrpXQO",
            "Autumn2023__64": "HA_rjkWYkWB"
        }
    }
```
<hr>

# Continue [here](./Question.md)