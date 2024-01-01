import subprocess
import os
from django.conf import settings
import secrets
from Contest.models import (Contest_Question,
                            Contests,
                            Contest_submissiosn,
                            Contest_Groups)
import re
import random, string
from Contest.tasks import scheduler
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache

class RunCode:
    def __init__(self,
                group,
                 question,
                 contest,
                 language,
                 file
                 ):
        self.group = group
        self.contest_name = contest.name 
        self.question_name = question.title
        self.language = language
        self.time_limit = question.time_limit
        self.last_solved = 0
        self.file = file,
        self.executableFiles = ["java","c","c++","ts","rust","c#"]
    

    def MakeExecutable(self,filepath,filename,lang):
        path = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(path)
        process_dic = {
            "java":{
                "name":filename,
                "exec_code":['javac', filepath]
            },
            "c#":{
                "name":filename[:-3],
                "exec_code":["mcs",filename]
            },
            "c":{
                "name":filename[:-2],
                "exec_code":['g++', filename,"-o",filename[:-2]]
            },
            "c++":{
                "name":filename[:-4],
                "exec_code":['g++', filename,"-o",filename[:-4]]
            },
            "rust":{
                "name":filename[:-3],
                "exec_code":["rustc",filename]
            },
            "ts":{
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
                "reason":"Error in here",
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
                    new_contents = contents.replace(f'class {current_class}', f'public class {filename[0:-5]}')
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
                "detail":"make sure you only have one valid class"
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
    
    def runCode(self,inputname,outputname,file,filename,lang):
        thispath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        os.chdir(os.path.dirname(thispath))
        language_commands = {
            "python": ["python3", file],
            "java": ["java", filename],
            "php": ["php", file],
            "c": ["./" + filename],
            "c++": ["./" + filename],
            "rust": ["./" + filename],
            "c#": ["./" + filename + ".exe"],
            "js": ["node", thispath],
            "ts": ["node", thispath],
        }

        try:
            process = subprocess.Popen(language_commands.get(lang, []),stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            path = os.path.join(settings.BASE_DIR,"files","contest",self.contest_name,self.question_name)
            os.chdir(path)
            with open(inputname, 'r') as input_file:
                    input_data = input_file.read().encode()
            try:
                output, error = process.communicate(input_data,timeout=self.time_limit)
            except subprocess.TimeoutExpired:
                process.kill()
                return False,{
                    "reason":"timeout"
                }
            if error:
                return False,{
                "reason":"Error",
                "error":str(error)
            }
            with open(outputname, 'r') as output_file:
                expected_output = output_file.read()
            print(f"expected_output was : {expected_output.strip()}")
            print()
            print(f"your output was {output.decode().strip()}")
            if output.decode().strip() == expected_output.strip():
                return True,{}
            else:
                return False,{
                    "reason":"InvalidAnswer",
                    "output":output.decode().strip(),
                    "expected_output":expected_output.strip()
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
            "c++":".cpp",
            "c":".c",
            "js":".js",
            "ts":".ts",
            "php":".php",
            "rust":".rs",
            "c#":".cs"
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
            if self.language == "c#":
                filename = filename + ".exe"
            self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))

    def run(self):
        compileResult,compileDetail = self.readyFiles()
        if not compileResult:
            return False,compileDetail
        file = compileDetail["file"]
        filename = compileDetail["filename"]
        # we loop on the number of testcases
        for i in range(1,self.num_of_test_cases+1):
            result ,detail = self.runCode(
                f"{self.contest_name}__{self.question_name}__input{i}.txt"
                ,f"{self.contest_name}__{self.question_name}__output{i}.txt"
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
        # TODO : Refactor has compiled files are deleted 
        """Since These Lanuages Compile with other data"""
        self.deleteCompiledData(filename)
        """Delete The Original File"""
        self.deleteFile(file)
        """If The User Solved A Question Then SetStatus To Solved"""

        return True,{}