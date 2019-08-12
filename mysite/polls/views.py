import numpy as np
import pandas as pd
import pymysql
import logging
import json
from sqlalchemy import create_engine
from datetime import datetime
from django.http import HttpResponse
from polls.response import Response
from polls.constants import Constants,TableColumn,Strategies
pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.DEBUG)


def index(request):
    logging.info('index() method running')
    response = Response()
    response.data = Constants.testMsg
    return HttpResponse(response)

def buildAssetClass(request):
    logging.info('buildAssetClass() method running')
    response = Response()
    try:
        asset_class = request.GET.get(Constants.ASSET_CLASS)

        df = pd.read_json(Constants.JSONPATH+asset_class+".json")
        securitylist = df[Constants.SECURITY]
        securitylist = list(securitylist.map(lambda x: {"value": x, "label": x}))

        response.data = {Constants.ASSET_CLASS:asset_class, Constants.SECURITY: list(securitylist)}
        return HttpResponse(response)
    except:
        response.errorCode = -1
        response.errorMsg = Constants.ERRORMSG
        logging.error(response.errorMsg)
        return HttpResponse(response)

#
# def runbanktest(request):
#     asset_class = request.GET.get('asset_class')
#     st = request.GET.get('start').split('-')
#     ed = request.GET.get('end').split('-')
#     start = datetime(int(st[0]),int(st[1]),int(st[2]))
#     end = datetime(int(ed[0]),int(ed[1]),int(ed[2]))
#     security = request.GET.get('security')
#     strategy = request.GET.get('strategy')
#     if strategy == "KAMA" :
#         result = KAMA(asset_class,security,start,end).to_json(orient='split')
#         result = '{"asset_class":'+asset_class+',"security:"'+security+',"result":'+result+'}'
#         return HttpResponse(result)
#     elif strategy == "MACD" :
#         result = MACD(asset_class,security,start,end).to_json(orient='split')
#         return HttpResponse(result)
#     return HttpResponse("Do not have this strategy")

def LoadAllDataFrames(asset_class,security, start, end):
    logging.info('LoadAllDataFrames() method running')
    engine = create_engine(Constants.SQLCONNECT)
    sql = Constants.getSQL(asset_class,security, start, end)
    data = pd.read_sql(sql, con=engine)
    data.reset_index()
    data.index = data[TableColumn.DATE]
    print(data.head())

    return data


def KAMA(asset_class,security, start, end):
    logging.info('KAMA() method running')
    df = LoadAllDataFrames(asset_class,security, start, end)
    df['Change'] = np.abs(df[TableColumn.CLOSE] - df[TableColumn.CLOSE].shift(10))
    df['Volatility'] = np.abs(df[TableColumn.CLOSE] - df[TableColumn.CLOSE].shift(1)).rolling(10).sum()
    df['ER'] = df['Change'] / df['Volatility']
    df['SC'] = (df['ER'] *(1/(1+1) - 1/(30+1)) + 1/(30+1))**2
    df[Strategies.KAMA]=0
    df[Strategies.KAMA][0] = df[TableColumn.CLOSE][0:10].mean()
    df[Strategies.KAMA] = df[Strategies.KAMA].shift(1) + df['SC'] * (df[TableColumn.CLOSE] - df[Strategies.KAMA].shift(1))
    thr = 0.0002
    df[TableColumn.REGIME]=0
    df[TableColumn.REGIME]=np.where((((df[Strategies.KAMA] - df[Strategies.KAMA].shift(1)) > thr) & ((df[Strategies.KAMA].shift(1) - df[Strategies.KAMA].shift(2)) > thr)), 1, 0)
    df[TableColumn.REGIME]=np.where((((df[Strategies.KAMA] - df[Strategies.KAMA].shift(1)) < -thr) & ((df[Strategies.KAMA].shift(1) - df[Strategies.KAMA].shift(2)) < -thr)), -1, df['Regime'])
    df[TableColumn.MARKET] = np.log(df[TableColumn.CLOSE] / df[TableColumn.CLOSE].shift(1))
    df[TableColumn.STRATEGY] = df[TableColumn.REGIME].shift(1)*df[TableColumn.MARKET]
    # return df[TableColumn.RESULTCOLS].cumsum().apply(np.exp)

def cal_macd(data,short_,long_,m):
    logging.info('cal_macd() method running')
    data['diff']=data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    
    data['dea']=data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    
    data['macd']=2*(data['diff']-data['dea'])
    return data



def MACD(asset_class,security, start, end):
    response = Response()
    logging.info('MACD() method running')
    df = LoadAllDataFrames(asset_class,security, start, end)
    df = df.sort_index(ascending=True)
    ### MACD Strategy 
     
    macd_data = cal_macd(df,12,26,9)  
    df['cal_diff']= macd_data['diff'] -macd_data['diff'].shift(1)
    df['cal_dea'] = macd_data['dea'] -macd_data['dea'].shift(1)
    df[TableColumn.REGIME]= np.where((df['cal_diff'] < 0) & (df['cal_dea'] < 0) , 1,0)
    df[TableColumn.REGIME]= np.where((df['cal_diff'] > 0) & (df['cal_dea'] > 0)  ,-1,df[TableColumn.REGIME])
    df[TableColumn.MARKET] =np.log( df[TableColumn.CLOSE]/df[TableColumn.CLOSE].shift(1))
    df[TableColumn.STRATEGY]=df[TableColumn.REGIME].shift(1)*df[TableColumn.MARKET]

    df[TableColumn.EXP_STRATEGY]=df[TableColumn.STRATEGY].cumsum().apply(np.exp)
    df[TableColumn.EXP_MARKET]=df[TableColumn.MARKET].cumsum().apply(np.exp)
    df[TableColumn.YIELD] = df[TableColumn.EXP_STRATEGY]-df[TableColumn.EXP_MARKET]
    res = df[TableColumn.YIELD][-1]
    response.data={Constants.ASSET_CLASS: asset_class, Constants.SECURITY:security,"poltData":list(df[TableColumn.RESULTCOLS]),TableColumn.YIELD:res}
    return response
    
    ###Strategy
def dual_thrust(data,K1,K2):
    logging.info('dual_thrust() method running')
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
