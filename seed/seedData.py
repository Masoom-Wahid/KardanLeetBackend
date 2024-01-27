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
        "NthFibonacciOfANumber":{
        "data" :{
        "num_of_test_cases":"5",
            "lvl":"HARD",
            "point":"30",
            "time_limit":"10",
            "description":"""Given int 'n' for testcases and str 'k' for num , find whether the given nth fibonacci sequence\n 
            The Fibonacci sequence is a series of numbers in which each number is the sum of the two preceding ones, usually starting with 0 and 1. The sequence goes: 0, 1, 1, 2, 3, 5, 8, and so forth.
            each nth is the sum of the n-1 and n-2""",
        },
            "testcases":{
                "input":"4\n4\n5\n6\n7\n",
                "output":"3\n5\n8\n13"
            },
            "samples":{
                "sample":"4",
                "answer":"2",
                "explanation":"Because 1+1 is 2",
            },
            "consts":{
                "consts":"n<=10\nk<10"
            }
        }
        }
        }