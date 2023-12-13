# Auth
<hr>

## Table Of Content
* ### [Creating Admins](#creating-admins)
* ### [Creating ContestGroups](#contest-group-and-user-creation)
* ### [Creating Alias For ContestGroups](#creating-alias)

<hr>

## Creating Admins
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
        "password":"password"
    }
```
<hr>

## Contest Group And User Creation
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

## Creating Alias
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
