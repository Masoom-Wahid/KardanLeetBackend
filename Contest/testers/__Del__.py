"""
Used For Not Deleted TestCases Which are created from compilation
and for some reason are not deleted after compilation.
this is regularly used when starting and finishing the contest to just clean up the folder
DELETE EVERYTHING IN "testers" folder except the exception array which is what is imporant for 
Contest
"""


import os


def deleteFiles(path=os.getcwd()
                ,exception=["__Del__.py",
                            "__init__.py",
                             "__pycache__",
                            "execute.py",
                            "ManualRun.py",
                            "Run.py",
                            "SubmitRun.py"]):
    
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in exception:
                os.remove(file_path)


if __name__ == "__main__":
    deleteFiles()