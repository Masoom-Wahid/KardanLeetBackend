# KardanLeet Documentation
### :star: An Offline Based Programming Contest Which Lets You To Judge and See The Result Of The Contests
* #### :rocket: Supported Languages
    * Python
    * C++
    * Rust
    * JavaScript
    * C
    * C#
    * Java
    * PHP
    * TypeScript

> \[!IMPORTANT]
>
> This Is The Setup Documenation If You Want API Documentation, Click [Here](./docs/Introduction.md).

## ERD
You Can View The ERD [Here](https://drawsql.app/teams/masooms-team/diagrams/kardanleet)
<hr>

### How To Setup?
#### You Can Either Do It By Docker or You Can Do It by Creating Your Own Venv

> \[!IMPORTANT]
>
> With Docker You Will Also Install Every Compiler Needed and without it the server can't function
> properly
#### [Docker](#setup-with-docker)
#### [Venv]()
#### Setup with Docker
#### Just Create The Docker Build and Run It , You Can Do So By
``` shell
make

```
#### if u want to change ur image and update to ur existing code after pulling the latest update from repo u can do so by
```shell
make build
```
#### if u want to run the docker after creating u can do so by
```shell
make docker-run
```
#### if u want to remove the image from your computer 
```shell
make docker-remove
```
<br>

#### Setup With Venv
#### Start By Creating A Virtual Env.
``` shell
python3 -m venv venv 

```
<hr>

* #### Run The Venv (This Can Differ Depending On Your OS)
#### Run The Venv (This Can Differ Depending On Your OS)
##### For Linux and Mac
``` shell
source ./venv/bin/activate

```
##### For Windows
```shell
venv\Scripts\activate
```

<hr>

* #### :white_check_mark:  If Everything Has Gone Correct and Now U Have Activated Your Venv
#### If Everything Has Gone Correct and Now U Have Activated Your Venv :white_check_mark: 
#### run this command when u are in the same dir as manage.py file and it should do all the work
```shell
make install-from-venv
```
<hr>

> \[!NOTE]
>
> This Program Requires You Have the compilers of all the languages said in the above
> To Check If You Have All Those Compilers Run:
```shell
make check-compilers
```
<br>

* ##### :white_check_mark: If Passed All The TestCases Start Reading API Documenation From [Here](./docs/Introduction.md)
* ##### :x: If Not Install The Said Compilers You Do Not Have
##### :white_check_mark: If Passed All The TestCases , Start Reading API Documenation From [Here](./docs/Introduction.md)
##### :x: If Not Install The Said Compilers You Do Not Have
<hr>


## :white_check_mark: Once You Setup The Repo Start Reading API Documenation From [Here](./docs/Introduction.md)






