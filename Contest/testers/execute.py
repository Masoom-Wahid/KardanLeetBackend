import subprocess
import os
from django.conf import settings
import secrets
from Contest.models import Contest_Question,Contests
import re
import random, string



class RunCode:
    def __init__(self,question_name,contest_name,language,extensions,file,num_of_test_cases=2,last_solved=0):
        self.last_solved = last_solved
        self.num_of_test_cases=num_of_test_cases
        self.contest_name = contest_name 
        self.question_name = question_name
        self.language = language
        self.extensions = extensions
        self.file = file
    
    def deleteFile(self,filename):
        os.remove(os.path.join("/",filename))
    

    def runJava(self,file,classname,question_path,question_name):
        testing_dir = os.path.join(settings.BASE_DIR,"Contest","testers")
        os.chdir(testing_dir)

        java_command = ['java','execute', self.num_of_test_cases,classname, f'{file}',question_path,question_name]
        process = subprocess.Popen(java_command)

        # Wait for the subprocess to complete and get the exit code
        exit_code = process.wait()

        # Use the exit code as the result returned from the Java program
        result = exit_code
        self.deleteFile(file)
        self.deleteFile(os.path.join(testing_dir,f"{classname}.class"))
        if result == 0:
            return [True]
        elif result == 2:
            return [False,"timeout","0"]
        else:
            return [False,"invalidAnswer"]
    
    def runPython(self,inputname,outputname,file):
        TIMEOUT = 10
        try:
            process = subprocess.Popen(['python3', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            with open(inputname, 'r') as input_file:
                input_data = input_file.read().encode()
            try:
                output, _ = process.communicate(input_data,timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                process.kill()
                return "timeout"
            with open(outputname, 'r') as output_file:
                expected_output = output_file.read()
            # print(output.decode().strip())
            # print(expected_output.strip())
            if output.decode().strip() == expected_output.strip():
                return True
            else:
                return False
            
        except Exception as e:
            return False
        


    
    def runC(self):
        pass
    
    def run(self):
        code = self.file.read()
        file = makethefile(code,self.extensions)
        languages = {"python": self.runPython, "java": self.runJava,"c":self.runC}
        compare_results = languages[self.language]
        path = os.path.join(settings.BASE_DIR,"files","contest",f"{self.contest_name}",f"{self.question_name}")
        if self.language != "python":
            class_changed_file = changeClassName(file)
            res = compare_results(file,class_changed_file,path,f"{self.contest_name}__{self.question_name}__")
            return res
        else:
            os.chdir(path)
            for run in range(1,self.num_of_test_cases+1):
                result = compare_results(f"{self.contest_name}__{self.question_name}__input{run}.txt"
                                        ,f"{self.contest_name}__{self.question_name}__output{run}.txt",
                                        file)
                if result == "timeout":
                    self.deleteFile(file)
                    return [False,"timeout",self.last_solved]
                elif not result:
                    self.deleteFile(file)
                    return [False,self.last_solved]
                else:
                    self.last_solved += 1
            # self.deleteFile(file)
            return [True,self.last_solved]








class SubmitCode:
    def __init__(self) -> None:
        pass

def changeClassName(filepath):
    choices = string.ascii_letters + string.ascii_lowercase
    newClassName = "".join(random.choice(choices) for i in range(8))
    with open(filepath, 'r+') as f:
        contents = f.read()
        match = re.search(r'class (\w+)\b', contents)
        current_class = match.group(1)

        new_contents = contents.replace(f'class {current_class}', f'class {newClassName}')

        f.seek(0)
        f.truncate()
        f.write(new_contents)

    f.close()
    
    return newClassName

def makethefile(file_code,suffix):
    filename = f"{secrets.token_urlsafe()}{suffix}"
    filepath = os.path.join(settings.BASE_DIR,"Contest","testers",filename)
    code = file_code.decode('utf-8') 
    with open(filepath, 'w') as f:
        f.write(code)
    return filepath





# def python_run(num_of_test_cases,contest_name,question_name,file):
#     print(num_of_test_cases)
#     res = []
#     path = os.path.join(settings.BASE_DIR,"files","contest",f"{contest_name}",f"{question_name}")
#     os.chdir(path)
#     python_file = file.read()
#     file = makethefile(python_file)
#     for run in range(1,num_of_test_cases+1):
#         thisres = compare_results(f"{contest_name}__{question_name}__input{run}.txt"
#                                 ,f"{contest_name}__{question_name}__output{run}.txt",
#                                 file)
#         return "timeout" if thisres == "timeout" else res.append(thisres)
#     os.remove(os.path.join("/",file))
#     return res
		  
