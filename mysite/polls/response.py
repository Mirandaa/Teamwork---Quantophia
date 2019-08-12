import json
class Response():

    def __init__(self):
        self.errorCode = 0
        self.data = {}
        self.errorMsg = ''
    def __str__(self):
        return json.dumps({"errorCode":self.errorCode,"errorMsg":self.errorMsg,"data":self.data})

    def to_string(self):
        return ""+json.dumps({"errorCode": self.errorCode, "errorMsg": self.errorMsg, "data": self.data})