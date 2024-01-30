import subprocess
import os
from django.conf import settings
import re
import random, string
from Questions.models import SampleTestCases

"""
    LIST OF ERRORS AND STATUSS AVAILABLE FOR COMPILATION
    'THE ERRORS ARE ALWAYS RETURNED IN 'reason' key value pair'

    IF THE STATUS IS 200 THEN THE USER HAVE SOLVED THE QUESTION

    IF IT IS 406 THEN THE USER HAS NOT SOLVED THE QUESTION AND IS PROBABLY 
    FACING ONE OF THESE SAID ERRORS

    IF IS IS 423 THEN IT IS PROBABLY THAT THE CONTEST HAS NOT STARTED YET or Has Finished
    IF IS IS 412 THEN the user has already solved the question

    If It is 404 then the question does not exist or the user does not have a group_instance(Contact Admin)
    ___________________________________________________________

    "timeout":"it says that the code is taking longer the time_limit vairable",

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    "InvalidAnswer":"The Output and Expected Output Are Not The Same",

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    "Class Issues":"Only For Java And C# , this is when they make 2 classes(FORBIDDEN)",

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    "Compilation Error":"Only For Compiled Lanuages such as ["java","c","cpp","typescript","rust","csharp"]
    This means that there is a syntax error and that particular language could not be compiled into byte code
    "

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    "Error":"This Probbably Happens Alot For Interperted Lanuages Since They Are Not Checked at Compile Time
    but rather at runTime. Any Syntax Error Should Be Reported Here
    "

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    "Exception":"This is almost always the code or the server error , this should be treated like the status
    of 500 and is alwyas the problem of the server and not the code
    "

"""


class RunCode:
    def __init__(self,
                group,
                 question,
                 contest,
                 language,
                 file
                 ):
        self.group = group
        self.question = question
        self.contest_name = contest.name 
        self.question_name = question.title
        self.language = language
        self.time_limit = question.time_limit
        self.last_solved = 0
        self.file = file,
        self.executableFiles = ["java","c","cpp","typescript","rust","csharp"]
    

    def MakeExecutable(self,filepath,filename,lang):
        path = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(path)
        process_dic = {
            "java":{
                "name":filename,
                "exec_code":['javac', filepath]
            },
            "csharp":{
                "name":filename[:-3],
                "exec_code":["mcs",filename]
            },
            "c":{
                "name":filename[:-2],
                "exec_code":['g++', filename,"-o",filename[:-2]]
            },
            "cpp":{
                "name":filename[:-4],
                "exec_code":['g++', filename,"-o",filename[:-4]]
            },
            "rust":{
                "name":filename[:-3],
                "exec_code":["rustc",filename]
            },
            "typescript":{
                "name":filename[0:-2] + "js",
                "exec_code":["tsc",filepath]
            }
        }
        exec_code , name = process_dic[lang]["exec_code"] ,process_dic[self.language]["name"]
        process = subprocess.Popen(exec_code, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        _,error = process.communicate()
        if error:
            return False,{
                "reason":"Compilation Error",
                "error":error.decode()
            }
        return True,name


    
    def changeClassName(self,filepath,filename):
        """Since Java Is The Most Useless Language
            I will have to change the public class name myself
            -- this will also give error if 2 public class found so 1 public class is allowed
        """
        try:
            with open(filepath, 'r+') as f:
                contents = f.read()
                match = re.search(r'class (\w+)\b', contents)
                current_class = match.group(1)
                if self.language == "java":
                    new_contents = contents.replace(f'class {current_class}', f'class {filename[0:-5]}')
                else:
                    new_contents = contents.replace(f'class {current_class}', f'class {filename[0:-5]}')
                f.seek(0)
                f.truncate()
                f.write(new_contents)

            f.close()
            
            return True,filename[0:-5]
        except Exception as e:
            return False,{
                "reason":"Class Issues",
                "error":"make sure you only have one valid class"
            }


    def makethefile(self,file_code,suffix):
        """Make the file with the given suffix and code"""
        choices = string.ascii_letters + string.ascii_lowercase
        newClassName = "".join(random.choice(choices) for i in range(5))
        
        filename = f"{newClassName}{suffix}"
        filepath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        code = file_code.decode('utf-8') 
        with open(filepath, 'w') as f:
            f.write(code)

        return filepath,filename,code
    

    """Used For Deleting the processed files"""
    deleteFile = lambda self,filename : os.remove(os.path.join("/",filename))
    
    def getLanguageCommands(self,lang,filename,file,path):
        language_commands = {
            "python": [settings.PYTHON_VARIABLE_NAME, file],
            "java": ["java", filename],
            "php": ["php", file],
            "c": ["./" + filename],
            "cpp": ["./" + filename],
            "rust": ["./" + filename],
            "csharp": ["./" + filename + ".exe"],
            "javascript": ["node", path],
            "typescript": ["node", path],
        }
        return language_commands[lang]

    def runCode(self,inputData,expectedOutputData,file,filename,lang):
        thispath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        os.chdir(os.path.dirname(thispath))

        command = self.getLanguageCommands(lang,filename,file,thispath)

        try:
            process = subprocess.Popen(command,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                output, error = process.communicate(inputData,timeout=self.time_limit)
            except subprocess.TimeoutExpired:
                process.kill()
                return False,{
                    "reason":"timeout",
                    "error":"Infinite Loop Or The Question Took Longer Then Time Limit"
                }
            if error:
                return False,{
                "reason":"Error",
                "error":str(error)
            }
            
            """Only Print the Ouputs to the terminal when u are in debug mode"""
            if settings.DEBUG:
                print(f"expected_output was : \n{str(expectedOutputData).strip()}")
                print(f"your output was:  \n{str(output.decode()).strip()}")

            """
            Sometimes The Output From The user may contain \r\n instead of the usual
            \n which would let the incorrect answer even though they solved the question
            """
            FINALED_OUTPUT=output.decode().replace('\r\n', '\n')
            if FINALED_OUTPUT.strip() == str(expectedOutputData).strip():
                return True, {}
            else:
                return False, {
                    "reason": "InvalidAnswer",
                    "output": output.decode().strip(),
                    "expected_output": str(expectedOutputData).strip()
                }

        except Exception as e:
            return False,{
                "reason":"Exception",
                "error":str(e)
            }
        
    def readyFiles(self):
        code = self.file.read()
        """Used For Dynamically Producing the file suffixes or extenstions and their functions"""
        suffixes = {
            "python":".py",
            "java":".java",
            "cpp":".cpp",
            "c":".c",
            "javascript":".js",
            "typescript":".ts",
            "php":".php",
            "rust":".rs",
            "csharp":".cs"
        }
        extension = suffixes[self.language]
        # Create the file in disk so that we can run it
        file , filename ,code = self.makethefile(code,extension)
        #These languag require 2 Step compilation to run
        
        # execute the files
        if self.language in self.executableFiles:
            if self.language == "java":
                changing_result,filename = self.changeClassName(file,filename)
                if not changing_result:
                    self.deleteFile(file)
                    return False,filename
            result,filename = self.MakeExecutable(file,filename,self.language)
            if not result:
                self.deleteFile(file)
                return False,filename
            
        return True,{
            "file":file,
            "filename":filename
            }


    def deleteCompiledData(self,filename):
        if self.language in self.executableFiles:
            if self.language == "java":
                filename = filename+".class"
            if self.language == "csharp":
                filename = filename + ".exe"
            self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))

    def run(self):
        compileResult,compileDetail = self.readyFiles()
        if not compileResult:
            return False,compileDetail
        file = compileDetail["file"]
        filename = compileDetail["filename"]
        testCasesData = {}
        testCases = SampleTestCases.objects.filter(question=self.question)
        for testcase in testCases:
            testCasesData[testcase.name] = testcase.testCase.replace('\r\n', '\n')
        # we loop on the number of testcases
        for i in range(1,self.num_of_test_cases+1):
            result ,detail = self.runCode(
                bytes(testCasesData[f'input{i}'].encode())
                ,f"{testCasesData[f'output{i}']}"
                ,file
                ,filename
                ,self.language
                )
            if result:
                self.last_solved += 1
            else:
                self.deleteFile(file)
                self.deleteCompiledData(filename)
                detail["amount_solved"] = self.last_solved
                return False,detail
        """Since These Lanuages Compile with other data"""
        self.deleteCompiledData(filename)
        """Delete The Original File"""
        self.deleteFile(file)

        return True,{}