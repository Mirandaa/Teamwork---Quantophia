
import pandas as pd
import pymysql
import logging
import time;
import json
from datetime import datetime,timedelta
from django.http import HttpResponse

from polls.empty.SecurityData import calcResult, SecurityData
from polls.empty.response import Response
from polls.empty.constants import Constants
from polls.utils.calculation import Calculation as calc
pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.DEBUG)


def index(request):
    response = Response()
    return HttpResponse(response)

def getResult(request):
    response = Response()
    response,list =getRequest(response, request)
    if(response.error['code'] == -1):
        return HttpResponse(str(response))
    result = []
    for item in list:
        result.append(item.getDict())
    response.data = {"securityData":result}
    logging.info(response.error)
    logging.info("data return success!")
    return HttpResponse(str(response))

def getRequest(response,request):
    if (request.method == 'POST'):
        logging.info("the POST method")
        data = json.loads(request.body.decode())
        securityDataList = []
        days,startTime,endTime = timeFormat(data)
        # modelFrequency = data['modelFrequency']

        for product in data['tableProductData']:
            date, marketdata, df = calc.getMarketData(product['assetClass'], product['security'], startTime,
                                                      endTime)
            if df.empty:
                response.error = {"code":-1,"message":str('sorry ,have no data for: {}-{} between {} and {}  ').format(product['assetClass'], product['security'], startTime,
                                                      endTime)}
                return response,[]
            #这里调用循环计算每个产品对应的多种策略的结果
            calcResultList = []

            for strategy in data['tableStrategyData']:
                response, stratName, regime, Performance,  Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = calc.run(response,product['assetClass'],product['security'],strategy,df,days)
                if response.error['code'] == -1:
                    logging.info("{}\t{}".format(response.error['code'],strategy))
                    response.error = {"code":0,"message":"server Strategies calculation error have miss the like  {}  request".format(strategy)}
                    continue
                res = calcResult(stratName ,list(regime), str("{}%").format(Performance),
                                 str("{}%").format(Market),
                                 str("{}%").format(round(Diff * 100, 2)),
                                 ("{}%").format(round(AnnualizedReturn*100,2)),
                                 round(MaxDrawdown, 3),
                                 round(Alpha, 3),
                                 round(Beta, 3),
                                 round(SharpeRatio, 3)
                                 ).getDict()

                calcResultList.append(res)
                # logging.info(strategy)
            securityData = SecurityData(date,product['security'],marketdata,calcResultList)
            securityDataList.append(securityData)

        return response,securityDataList
    else:
        response.error =  {"code":-1,"message":'PostRequestList erro'}
        logging.error(response.error)
        return response ,[]

def timeFormat(data):
    start = data['startTime']
    interval = int(data['interval'])

    st = start.split('-')
    # ed = end.split('-')
    startTime = datetime(int(st[0]), int(st[1]), int(st[2]))
    endTime = startTime + timedelta(days = interval)
    days = interval
    return days,startTime,endTime


def buildAssetClass(request):
    logging.info('buildAssetClass() method running time: '+str(time.asctime( time.localtime(time.time()) )))
    response = Response()
    try:
        asset_class = request.GET.get(Constants.ASSET_CLASS)

        df = pd.read_json(Constants.JSONPATH+asset_class+".json")
        securitylist = df[Constants.SECURITY]
        securitylist = list(securitylist.map(lambda x: {"value": x, "label": x}))
        response.data = {Constants.ASSET_CLASS:asset_class, Constants.SECURITY: list(securitylist)}
        return HttpResponse(str(response))
    except:
        response.error = {"code":-1,"message":Constants.ERRORMSG}
        logging.error(Constants.ERRORMSG)
        return HttpResponse(str(response))




