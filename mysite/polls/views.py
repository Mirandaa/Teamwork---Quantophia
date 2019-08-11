
import numpy as np
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
import os
from datetime import datetime
from datetime import timedelta
# Create your views here.
from django.http import HttpResponse
dict = {}
f = open('polls/data/FOREX.json', 'r')
FOREX = f.read()
f = open('polls/data/IntradayNYSEMS7.json', 'r')
IntradayNYSEMS7 = f.read()
f = open('polls/data/LIFFE_FuturesOptions.json', 'r')
LIFFE_FuturesOptions = f.read()
f = open('polls/data/NASDAQ.json', 'r')
NASDAQ = f.read()
dict["FOREX"] = FOREX
dict["IntradayNYSEMS7"] = IntradayNYSEMS7
dict["LIFFE_FuturesOptions"] = LIFFE_FuturesOptions
dict["NASDAQ"] = NASDAQ
def index(request):
    return HttpResponse("Welcom BackTest!!!")
def buildAssetClass(request):
    print("+++++++++")
    asset_class = request.GET.get('asset_class')
    result = ""+str(dict[asset_class])
    return HttpResponse(result)
def runbanktest(request):
    asset_class = request.GET.get('asset_class')

    st = request.GET.get('start').split('-')
    ed = request.GET.get('end').split('-')
    start = datetime(int(st[0]),int(st[1]),int(st[2]))
    end = datetime(int(ed[0]),int(ed[1]),int(ed[2]))
    security = request.GET.get('security')
    strategy = request.GET.get('strategy')
    if strategy == "KAMA" :
        result = KAMA(asset_class,security,start,end).to_json(orient='split')
        result = '{"asset_class":'+asset_class+',"security:"'+security+',"result":'+result+'}'
        return HttpResponse(result)
    elif strategy == "MACD" :
        result = MACD(asset_class,security,start,end).to_json(orient='split')
        return HttpResponse(result)
    return HttpResponse("Do not have this strategy")

def LoadAllDataFrames(asset_class,security, start, end):
    
    dfs = pd.DataFrame()

    engine = create_engine('mysql://root:@localhost/mysql1')
    sql = "select date, ticker,open,high,low,close,vol from "+asset_class+" where date > '"+str(start)+" ' and date < '"+str(end)+"' and ticker = '"+security+"';"

    data = pd.read_sql(sql, con=engine)
    data.reset_index()
    data.index = data['date']
    print(data.head())

    return data

    return dfs

def KAMA(asset_class,security, start, end):
    
    df = LoadAllDataFrames(asset_class,security, start, end)
    df['Change'] = np.abs( df['close'] - df['close'].shift(10))
    df['Volatility'] = np.abs( df['close'] - df['close'].shift(1)).rolling(10).sum()
    df['ER'] = df['Change'] / df['Volatility']
    df['SC'] = (df['ER'] *(1/(1+1) - 1/(30+1)) + 1/(30+1))**2
    df['KAMA']=0
    df['KAMA'][0] = df['close'][0:10].mean()
    df['KAMA'] = df['KAMA'].shift(1)+df['SC']*(df['close'] - df['KAMA'].shift(1))
    thr = 0.0002
    df['Regime']=0
    df['Regime']=np.where((((df['KAMA'] - df['KAMA'].shift(1))>thr) & ((df['KAMA'].shift(1) - df['KAMA'].shift(2))>thr)),1,0)
    df['Regime']=np.where((((df['KAMA'] - df['KAMA'].shift(1))< -thr )& ((df['KAMA'].shift(1) - df['KAMA'].shift(2))< -thr)),-1,df['Regime'])
    df['Market'] = np.log(df['close'] / df['close'].shift(1))
    df['Strategy'] = df['Regime'].shift(1)*df['Market']
    cols = ['Market','Strategy']
    return df[cols].cumsum().apply(np.exp)

def cal_macd(data,short_,long_,m):
    data['diff']=data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    
    data['dea']=data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    
    data['macd']=2*(data['diff']-data['dea'])
    return data



def MACD(asset_class,security, start, end):
    
    df = LoadAllDataFrames(asset_class,security, start, end)

    df = df.sort_index(ascending=True)    
   
    ### MACD Strategy 
     
    macd_data = cal_macd(df,12,26,9)  
    df['cal_diff']= macd_data['diff'] -macd_data['diff'].shift(1)
    df['cal_dea'] = macd_data['dea'] -macd_data['dea'].shift(1)
    df['Regime']= np.where((df['cal_diff'] < 0) & (df['cal_dea'] < 0) , 1,0)
    df['Regime']= np.where((df['cal_diff'] > 0) & (df['cal_dea'] > 0)  ,-1,df['Regime'])   
    df["Market"] =np.log( df['close']/df['close'].shift(1))
    df['Strategy']=df['Regime'].shift(1)*df['Market']

    df['exp_Strategy']=df['Strategy'].cumsum().apply(np.exp)
    df['exp_Market']=df["Market"].cumsum().apply(np.exp)
    df['Yield'] = df['exp_Strategy']-df['exp_Market']
    res = df['Yield'][-1]

    return df[['exp_Strategy','exp_Market']]
    
    ###Strategy
def dual_thrust(data,K1,K2):
    HH = max(data['<high>'])
    LC = min(data['<close>'])
    HC = max(data['<close>'])
    LL = min(data['<low>'])
    # 获取 Range
    Range = max((HH-LC),(HC-LL))
    # 计算BuyLine 和 SellLine
    data['BuyLine'] = data['<open>'] + K1 * Range
    data['SellLine'] = data['<open>'] - K2 * Range
    data['Regime']= np.where( data['<close>'] < data['SellLine'] ,1,0)
    #data['Regime']= np.where( (data['<close>']-data['<close>'].shift(1))/data['<close>'].shift(1)>=0.02 , 1,0)
    data['Regime']= np.where( data['<close>'] > data['BuyLine'] , -1,data['Regime'])
    data["Market"] =np.log( data['<close>']/data['<close>'].shift(1))
    data['Strategy']=data['Regime'].shift(1)*data['Market']
    data['exp_Strategy']=data['Strategy'].cumsum().apply(np.exp)
    data['exp_Market']=data["Market"].cumsum().apply(np.exp)
    data['payoff'] = data['exp_Strategy']-data['exp_Market']
    return data
