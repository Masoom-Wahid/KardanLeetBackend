import subprocess
import os
from django.conf import settings
import tempfile
from Contest.models import Contest_Question,Contests



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

            if output.decode().strip() == expected_output.strip():
                return True
            else:
                return False
            
        except Exception as e:
            print("Error:", str(e))
        
    def runJava(self):
        pass
    def runC(self):
        pass
    
    def run(self):
        path = os.path.join(settings.BASE_DIR,"files","contest",f"{self.contest_name}",f"{self.question_name}")
        os.chdir(path)
        code = self.file.read()
        file = makethefile(code,self.extensions)
        languages = {"python": self.runPython, "java": self.runJava,"c":self.runC}
        compare_results = languages[self.language]
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
        self.deleteFile(file)
        return [True,self.last_solved]








class SubmitCode:
    def __init__(self) -> None:
        pass

def makethefile(python_code,suffix):
    tmp = tempfile.NamedTemporaryFile(suffix='.py', delete=False) 

    # Write code to file  
    tmp.write(python_code)

    # Close and get filename
    tmp.close()
    filename = tmp.name
    return filename




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
		  