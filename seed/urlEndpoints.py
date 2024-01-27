"""URL ENDPOINTS USED FOR SEED.PY"""
BASEURL = "http://127.0.0.1:8000/api"
UrlEndpoints = {
    "auth":f"{BASEURL}/auth/token/",
    "createContest":f"{BASEURL}/contest/",
    "createQuestions":f"{BASEURL}/questions/",
    "createTestCases":f"{BASEURL}/questions/testcases/",
    "createSamples":f"{BASEURL}/samples/",
    "createConstraints":f"{BASEURL}/constraints/",
    "assignQuestions":f"{BASEURL}/contest/setQuestions/",
    "createGroup":f"{BASEURL}/auth/users/",
    "actions":f"{BASEURL}/contest/actions/"
}