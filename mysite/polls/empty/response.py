import json
class Response():

    def __init__(self):
        self.error = {"code":0,"message":''}
        self.data = {}
    def getDict(self):
        return json.dumps({"error": self.error, "data": self.data})
    def __str__(self):
        return json.dumps(dict({"error":self.error,"data":self.data}))
