API Documentation
Authentication
Login

    POST /api/auth/token/
        Requires:
            username
            password
        Returns: access and refresh JWT tokens

Refresh Token

    POST /api/auth/token/refresh/
        Requires: refresh token
        Returns: refreshed access token

Creating Users

    POST /api/auth/users/
        permissions -> superuser
        Requires:
            type -> normal,contest
        _________________________________________________________________________________
        if normal : requires username and password -> it will create a superuser 
        ____________________________________________________________________________
        if contest : requires amount and contest_id -> will create user and group to the 
        given amount (ie : if 20 it will create 20 users) 
        it will also create contestant_groups to the given amount and will return 
        username and password of the created users and contestant_group


Contest
<div style="background-color:#eee; padding: 10px;">
Create Contests

    POST /api/contest/
        permissions -> superuser
        requires -> name,duration -> (04:00:00) meaning 4 hours
        will create a contest 
        Note: the name should be unique

List Groups

    GET /api/contest/groups/
        permissions -> superuser
        requires -> name (contest_name)
        returns all the groups in the contest

List Contestants

    GET /api/contest/contestants/
        permissions -> superuser
        requires -> group_id in param /api/contests/contestants?group_id=<id>
        return all the contestants in that particular group
    ____________________________________________________________________________
    POST /api/contest/contestants/
        permissions -> superuser
        requires -> group_id and name
        creates a contestants in that particular group
    DELETE /api/contests/contestants/
        permissions -> superuser
        requires -> id
        delete that particular contestants
</div>
Questions
<div style="background-color:#eee; padding: 10px;">
List Questions

    GET /api/questions/
        requires -> name (contest_name) in param
        /api/questions?name=<contest_name>
        returns all the questions in the contest
    ____________________________________________________________________
    POST /api/questions/
        requires -> name(contest_name) , title , lvl(HARD,MEDUIM,EASY), description , num_of_test_cases
    Note : num_of_test_cases will be number of testcases as a total
    ____________________________________________________________________
    POST /api/questions/test_cases/
        It Creates sample_test_cases which will be shown to the user in the decsription of the question
        this is not the real test_cases
        requires -> id(question_id) , sample , answer
    _____________________________________________________________________
    POST /api/questions/test_cases_files/
        requires -> id , files as list
        if the num_of_test_cases is 3
        the files should be :
        files : input1.txt
        files : output1.txt
        files : input2.txt
        files : output2.txt
        files : input3.txt
        files : output3.txt
        Note : the ordering isnt important but all the files should be in there otherwise the server will
        give an error 500
        not that being as input1.txt and output1.txt is important
</div>

