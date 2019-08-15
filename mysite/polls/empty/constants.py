class Constants:

    ASSET_CLASS = 'asset_class'
    SECURITY = 'security'
    SQLCONNECT = "mysql://root:Abcd1234@localhost/mysql1"
    ERRORMSG = 'buildAssetClass() return  security[] error'
    JSONPATH = "polls/data/"
    testMsg = {"data":"Welcom BackTest!!!"}
    STOCK = ""
    def getSQL(self,asset_class,security, start, end):
        return "select distinct date, ticker,open ,high,low,close,vol from "+asset_class+" where date > '"\
          +str(start)+"' and date < '"+str(end)+"' and ticker = '"+security+"';"

class TableColumn:
    DATE = 'date'
    TICKER= 'ticker'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
    OPEN = 'open'
    VOL = 'vol'
    OI = 'oi'
    REGIME = "Regime"
    MARKET = "Market"
    STRATEGY = "Strategy"
    EXP_STRATEGY = "exp_Strategy"
    EXP_MARKET = "exp_Market"
    YIELD = "Yield"
    RESULTCOLS = [DATE,EXP_STRATEGY, EXP_MARKET]
class Strategies:
    KAMA = 'KAMA'
    MACD = 'MACD'
    DualThrust ="DualThrust"
    SimpleMultiAverage="SimpleMultiAverage"
    KDJ = "KDJ"
    LogisticRegression = "LogisticRegression"

