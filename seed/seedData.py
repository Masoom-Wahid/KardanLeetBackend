CONTEST_NAME = "Winter2023"
SEED_DATA = {
    "contestDetail":{
        "contestName":CONTEST_NAME,
        "duration":"00:10:00"
    },
    "questionsDetail":{
        "FactorialOfANumber":{
        "data" :{
            "num_of_test_cases":"5",
            "lvl":"MEDUIM",
            "point":"20",
            "time_limit":"10",
            "description":"Given int 'n' for testcases and int 'k' for numbers , find the factorial of 'n' and print the output",
            },
            "testcases":{
                "input":"4\n3\n3\n4\n5\n",
                "output":"6\n6\n24\n120"
            },
            "samples":{
                "sample":"5",
                "answer":"120",
                "explanation":"Because Factorial Of 5 is 120",
            },
            "consts":{
                "consts":"n<=10\nk<2**10"
            }

        },
        "FindThePalindrome":{
        "data" :{
        "num_of_test_cases":"5",
            "lvl":"EASY",
            "point":"10",
            "time_limit":"10",
            "description":"Given int 'n' for testcases and str 'k' for word , find whether the given word is palindrome or not",
            },
            "testcases":{
                "input":"3\nwow\nbob\nnot\n",
                "output":"True\nTrue\nFalse"
            },
            "samples":{
                "sample":"wow",
                "answer":"True",
                "explanation":"Because 'wow' reversed is 'wow' and it is a palindrome",
            },
            "consts":{
                "consts":"n<=10\nk<10"
            }
        },
        "TwoSum":{
        "data" :{
        "num_of_test_cases":"5",
            "lvl":"HARD",
            "point":"30",
            "time_limit":"5",
            "description":"""Given an array of integers 'nums' and an integer 'target', return indices of the
            two numbers such that they add up to 'target'.
            """,
        },
            "testcases":{
                "input":"2\n9\n2 7 11 15\n3\n1 7 2 1",
                "output":"0 1\n0 2"
            },
            "samples":{
                "sample":"1\n9\n2 7 11 15",
                "answer":"0 1",
                "explanation":"Because nums[0] + nums[1] is 9",
            },
            "consts":{
                "consts":"nums.length<=10\ntarget<=100"
            }
        }
        }
        }