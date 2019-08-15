import json


class Product:
    '''
    def init()
    :param assetClass: product assetClass, str type
    :param security: product security , str type
    '''
    def __init__(self,assetClass,security):
        self.assetClass = assetClass
        self.security = security
    def __str__(self):
        return json.dumps(dict({"assetClass":self.assetClass,"security":self.security}))


class Strategy:
    def __init__(self,strategy):
        self.strategy = strategy
    def __str__(self):
        return json.dumps(dict({"strategy":self.strategy}))
