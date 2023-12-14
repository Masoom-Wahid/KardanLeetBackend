from .execute import RunCode
from django.conf import settings
import os
import subprocess
class ManualRun(RunCode):
    def __init__(self,group,question,contest,language,file,manual_testCase):
        super().__init__(group,question,contest,language,file)
        self.file = file
        self.manual_testCase = manual_testCase
        self.num_of_test_cases=1

        
    def runCode(self,file,filename,lang):
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
 
            input_data = self.manual_testCase.encode()
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
            return True,{
                "output":output.decode().strip()
            }
        except Exception as e:
            return False,{
                "reason":"Exception",
                "error":str(e)
            }
        
    
    def run(self):
        compileResult,compileDetail = self.readyFiles()
        if not compileResult:
            return False,compileDetail
        file = compileDetail["file"]
        filename = compileDetail["filename"]
        result ,detail = self.runCode(
                                file
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
        self.deleteCompiledData(filename)
        self.deleteFile(file)

        return True,detail

