from .execute import RunCode
class Run(RunCode):
    def __init__(self,group,question,contest,language,file):
        super().__init__(group,question,contest,language,file)
        self.file = file
        self.num_of_test_cases= 2
        self.manual_testCase = None
