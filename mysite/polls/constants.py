class Constants:

    ASSET_CLASS = 'asset_class'
    SECURITY = 'security'
    SQLCONNECT = "mysql://root:@localhost/mysql1"
    ERRORMSG = 'buildAssetClass() return  security[] error'
    JSONPATH = "polls/data/"
    testMsg = {"msg":"Welcom BackTest!!!"}
    def getSQL(self,asset_class,security, start, end):
        return "select date, ticker,open ,high,low,close,vol from "+asset_class+" where date > '"\
          +str(start)+" ' and date < '"+str(end)+"' and ticker = '"+security+"';"

class TableColumn:
    DATE = 'date'
    TICKER= 'ticker'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
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
    KAMA = 'kama'
    MACD = 'macd'
