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
        self.obj = Contest_submissiosn.objects.create(
            id = self.makeId(),
            group = group,
            question = question,
            lang=language,    
            code = "",
            status=""
        )
    def writeCode(self,file):
        self.obj.code = file
        self.obj.save()
    
    def setStatus(self,status):
        self.obj.status = status
        self.obj.save()


    def solved(self):
        self.obj.solved = True
        self.obj.status = "Solved"
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

    def getLangDetails(self,lang):
        """Used For Dynamically Producing the file suffixes or extenstions and their functions"""
        suffixes = {
            "python":".py",
            "java":".java",
            "c++":".cpp",
            "c":".c",
            "js":".js",
            "ts":".ts"
        }
        languages = {
            "python": self.runPython,
            "java": self.runJava,
            "c":self.runC,
            "c++":self.runC,
            "js":self.runJs,
            "ts":self.runJs
            }

        return suffixes[lang],languages[lang]
    
    def makeCExec(self,filepath,filename):
        """Makes the c file executable using g++"""
        path = os.path.join(settings.BASE_DIR,"Contest","testers")
        if self.language == "c++":
            name = filename[:-4]
        else:
            name = filename[:-2]
        os.chdir(path)
        process = subprocess.Popen(['g++', filename,"-o",name], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
        """
        with open(filepath, 'r+') as f:
            contents = f.read()
            match = re.search(r'class (\w+)\b', contents)
            current_class = match.group(1)

            new_contents = contents.replace(f'class {current_class}', f'class {filename[0:-5]}')

            f.seek(0)
            f.truncate()
            f.write(new_contents)

        f.close()
        
        return filename[0:-5]

    def makethefile(self,file_code,suffix):
        """Make the file with the given suffix and code"""
        choices = string.ascii_letters + string.ascii_lowercase
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
    
    def runJs(self,inputname,outputname,file,filename):
        path = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        try:
            process = subprocess.Popen(['node',path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            path = os.path.join(settings.BASE_DIR,"files","contest",self.contest_name,self.question_name)
            os.chdir(path)
            with open(inputname, 'r') as input_file:
                input_data = input_file.read().encode()
            try:
                output, error = process.communicate(input_data,timeout=self.time_limit)
            except subprocess.TimeoutExpired:
                process.kill()
                return "timeout"
            if error:
                return False,{
                "reason":"Error",
                "error":str(e)
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

    def runJava(self,file,classname,question_name):
        question_path = os.path.join(settings.BASE_DIR,"files","contest",f"{self.contest_name}",f"{self.question_name}")
        testing_dir = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(testing_dir)
        java_command = ["java",'execute',str(self.num_of_test_cases),classname, f'{file}',question_path,question_name]
        process = subprocess.Popen(java_command)
        exit_code = process.wait()
        self.deleteFile(file)
        self.deleteFile(os.path.join(testing_dir,f"{classname}.class"))
        if exit_code == 0:
            self.submission.solved()
            return [True]
        elif exit_code == 2:
            return [False,"timeout","0"]
        else:
            return [False,"invalidAnswer"]
    
    def runPython(self,inputname,outputname,file,filename):
        question_path = os.path.join(settings.BASE_DIR,"files","contest",f"{self.contest_name}",f"{self.question_name}")
        os.chdir(question_path)
        try:
            #TODO : make the python3 varibale name dynamic from settings
            process = subprocess.Popen(['python3', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
                "error":str(e)
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
        


    
    def runC(self,inputname,outputname,file,filename):
        thispath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
        os.chdir(os.path.dirname(thispath))
        try:
            process = subprocess.Popen(f"./{filename}", stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
                "error":str(e)
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
        
    def makeJs(self,file,filename):
        """Makes a javascript file out of typescript"""
        path = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(path)
        process = subprocess.Popen(["tsc",file],stderr=subprocess.PIPE)
        process.wait()
        _ , error = process.communicate()
        if error:
            return False,{
                "reason":"Error",
                "error":error.decode()
            }
        res_filename = filename[0:-2] + "js"
        return True,res_filename
    
    def run(self):
        code = self.file.read()
        extension , compare_results = self.getLangDetails(self.language)
        file , filename = self.makethefile(code,extension)
        
        if self.language == "java":
            class_changed_file = self.changeClassName(file,filename)
            result,detail = compare_results(file,class_changed_file,f"{self.contest_name}__{self.question_name}__")
            return result,detail
        else:
            if self.language == "c" or self.language == "c++":
                result , filename = self.makeCExec(file,filename)
                if not result:
                    return False,filename
            elif self.language == "ts":
                result ,filename = self.makeJs(file,filename)
                if not result:
                    return False,filename
            for i in range(1,self.num_of_test_cases+1):
                result ,detail = compare_results(
                    f"{self.contest_name}__{self.question_name}__input{i}.txt"
                    ,f"{self.contest_name}__{self.question_name}__output{i}.txt"
                    ,file
                    ,filename)
                if result:
                    self.last_solved += 1
                else:
                    self.deleteFile(file)
                    if self.language == "c++" or self.language == "c" or self.language == "ts":
                        self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))
                    detail["amount_solved"] = self.last_solved
                    return False,detail
            """Since These Lanuages Compile with other data"""
            if self.language == "c++" or self.language == "c" or self.language == "ts":
                self.deleteFile(os.path.join(settings.BASE_DIR,"Contest","testers",filename))
            
            self.deleteFile(file)
            if self.type == "submit" : self.submission.solved()
            return True,{}