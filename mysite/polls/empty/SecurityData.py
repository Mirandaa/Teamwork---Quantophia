import json
class SecurityData:
    def __init__(self,date = [],secName = '',marketData = [],calcResult = [] ):
        self.date = date
        self.secName = secName
        self.marketData = marketData
        self.calcResult = calcResult
    def getDict(self):
        return {"secName":self.secName ,"date": self.date,"marketData":self.marketData ,"calcResult":self.calcResult}
    def __str__(self):
        return json.dumps({"secName":self.secName ,"date": self.date,"marketData":self.marketData ,"calcResult":self.calcResult})

class calcResult:
    def __init__(self, stratName ,regime, Performance,Market,Diff,AnnualizedReturn,MaxDrawdown,Alpha,Beta,SharpeRatio):
        self.stratName = stratName
        self.regime = regime
        self.Performance = Performance
        self.Market = Market
        self.Diff = Diff
        self.AnnualizedReturn = AnnualizedReturn
        self.MaxDrawdown = MaxDrawdown
        self.Alpha = Alpha
        self.Beta = Beta
        self.SharpeRatio = SharpeRatio
    def getDict(self):
        return {"stratName":self.stratName ,"regime":self.regime,"Performance":self.Performance,"Market":self.Market,"Diff":self.Diff,"AnnualizedReturn":self.AnnualizedReturn,"MaxDrawdown":self.MaxDrawdown,"Alpha":self.Alpha,"Beta":self.Beta,"SharpeRatio":self.SharpeRatio}
    def __str__(self):
        return json.dumps(self.getDict())


