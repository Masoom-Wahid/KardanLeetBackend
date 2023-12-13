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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




class MakeSubmissions:
    def makeId(self):
        token = secrets.token_urlsafe(16)
        while Contest_submissiosn.objects.filter(id=token).exists():
            token = secrets.token_urlsafe(16)
        return token
    def __init__(self,group,question,language):
        self.group = group
        self.question = question
        self.language = language
        self.runTime = timezone.now() + timedelta(seconds=2)
        self.obj = Contest_submissiosn.objects.create(
            id = self.makeId(),
            group = group,
            question = question,
            lang=language,    
            code = "",
            status=""
        )

    def updateLeaderboard(self,instance):
        leaderboard_obj = cache.get("leaderboard")
        if leaderboard_obj != None:
            
            stats = {
                "id":self.group.id,
                "point":self.group.calculateTotalPoint(),
                "time":self.group.calculateTime(),
                "penalty":self.group.calculatePenalty()
            }
            leaderboard_obj[self.group.group_name] = stats
            cache.set("leaderboard",leaderboard_obj)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("leaderboard", {"type": "Leaderboard.update","update":leaderboard_obj})
        else:
            pass        



    def writeCode(self,file):
        self.obj.code = file
        self.obj.save()
    
    def setStatus(self,status):
        if status == "Solved":
            self.obj.solved = True
        self.obj.status=status
        scheduler.add_job(self.updateLeaderboard, 'date',[self.obj], run_date=self.runTime,id=self.obj.id)
        self.obj.save()




class RunCode:
    def __init__(self,
                 type,
                group,
                 question,
                 contest,
                 language,
                 file,
                 last_solved=0):
        
        self.type = type
        if type == "submit":
            self.submission = MakeSubmissions(group,question,language)
        self.last_solved = last_solved
        self.num_of_test_cases=question.num_of_test_cases if type == "submit" else 2
        self.contest_name = contest.name 
        self.question_name = question.title
        self.language = language
        self.time_limit = question.time_limit
        self.file = file
    

    def MakeExecutable(self,filepath,filename,lang):
        path = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(path)
        if lang == "java":
            name = filename
            process = subprocess.Popen(['javac', filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif lang == "c#":
            name = filename[:-3]
            process = subprocess.Popen(["mcs",filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif lang == "c" or lang == "c++":
            name = filename[:-2] if lang == "c" else filename[:-4]
            process = subprocess.Popen(['g++', filename,"-o",name], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif lang == "rust":
            name = filename[:-3]
            process = subprocess.Popen(["rustc",filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif lang == "ts":
            process = subprocess.Popen(["tsc",filepath],stderr=subprocess.PIPE)
            name = filename[0:-2] + "js"
        process.wait()
        _,error = process.communicate()
        if error:
            return False,{
                "reason":"Error",
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
        newClassName = "".join(random.choice(choices) for i in range(8))
        if newClassName == "execute":
            newClassName = "".join(random.choice(choices) for i in range(8))
        
        filename = f"{newClassName}{suffix}"
        filepath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        code = file_code.decode('utf-8') 
        if self.type == "submit" : self.submission.writeCode(code)
        with open(filepath, 'w') as f:
            f.write(code)

        return filepath,filename
    

    """Used For Deleting the processed files"""
    deleteFile = lambda self,filename : os.remove(os.path.join("/",filename))
    
    def runCode(self,inputname,outputname,file,filename,lang):
        thispath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        os.chdir(os.path.dirname(thispath))
        try:
            if lang == "python":
                process = subprocess.Popen(['python3', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            elif lang == "java":
                process = subprocess.Popen(["java",filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            elif lang=="php":
                process = subprocess.Popen(['php', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            elif lang == "c" or lang == "c++" or lang == "rust":  
                process = subprocess.Popen(f"./{filename}", stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            elif lang == "c#":
                process = subprocess.Popen(f"./{filename}.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            elif lang == "js" or lang == "ts":
                process = subprocess.Popen(['node',thispath], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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
            # print(output.decode().strip())
            # print(expected_output.strip())
            if output.decode().strip() == expected_output.strip():
                return True,{}
            else:
                return False,{
                    "reason":"invalidAnswer",
                    "output":output.decode().strip(),
                    "expected_output":expected_output.strip()
                }
        except Exception as e:
            return False,{
                "reason":"Exception",
                "error":str(e)
            }
        

    def run(self):
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
        file , filename = self.makethefile(code,extension)
        #These languag require 2 Step compilation to run
        executableFiles = ["java","c","c++","ts","rust","c#"]
        # execute the files
        if self.language in executableFiles:
            if self.language == "java":
                changing_result,filename = self.changeClassName(file,filename)
                if not changing_result:
                    self.deleteFile(file)
                    return False,filename
            result,filename = self.MakeExecutable(file,filename,self.language)
            if not result:
                self.deleteFile(file)
                return False,filename
            
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
                if self.language == "c++" or self.language == "c" or self.language == "ts":
                    self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))
                detail["amount_solved"] = self.last_solved
                if self.type == "submit" : self.submission.setStatus(detail["reason"])
                return False,detail
            
        """Since These Lanuages Compile with other data"""
        if self.language in executableFiles:
            if self.language == "java":
                filename = filename+".class"
            if self.language == "c#":
                filename = filename + ".exe"
            self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))
        """Delete The Original File"""
        self.deleteFile(file)
        """If The User Solved A Question Then SetStatus To Solved"""
        if self.type == "submit" : self.submission.setStatus("Solved") 
        return True,{}