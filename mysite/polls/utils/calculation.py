from datetime import datetime
import numpy as np
import pymysql
import logging
import time;
import pandas as pd
from polls.utils.loadData import LoadData as load
from polls.empty.constants import TableColumn,Strategies
import sklearn
from sklearn import linear_model

pymysql.install_as_MySQLdb()

class Calculation:

    # 具体策略对应的 calcResult从这里返回
    def run(response,assetClass,security,strategy,df,days):
        try:
            if strategy == 'DT':
                return Calculation.DualThrust(response,df,days)
            elif strategy == 'SMA':
                return Calculation.SimpleMultiAverage(response,df, days)
            elif strategy == 'KDJ':
                return Calculation.KDJ(response,df, days)
            elif strategy == 'MACD':
                return Calculation.MACD(response,df, days)
            elif strategy == 'KAMA':
                return Calculation.KAMA(response,df, days)
            elif strategy == 'LR':
                train_df = Calculation.getTrainData(assetClass, security)
                return Calculation.LogisticRegression(response,df, days,train_df)
            else:
                response.error = {"code":-1,"message":'have no strategy called {}'.format(strategy)}
                logging.error("{} not exist! \t time: {}".format(strategy,str(time.asctime( time.localtime(time.time())))))
        except:
            logging.error("{} - Strategy calculation error ,the data may have some problems".format(strategy))
            return Calculation.calcErroe(response,strategy)
    def calcErroe(response,strategy):
        response.error = {"code":-1,"message":"{} Strategy calculation error ,the data may have some problems".format(strategy)}
        return response,strategy, 0, 0, 0, 0, 0, 0, 0, 0, 0
    # SecurityData 所需要的产品特有数据来自这里
    def getMarketData(asset_class, security, start, end):
        try:

            df = load.LoadAllDataFrames(asset_class, security, start, end)
            print(df.head())
            if df.empty:
                logging.error("loadData empty")
                return [],[],pd.DataFrame()
        except Exception as e:
            logging.error("loadData ERROE :{}".format(e))
            return [], [], pd.DataFrame()

        # print(df.head())

        df[TableColumn.MARKET] = np.log(df[TableColumn.CLOSE] / df[TableColumn.CLOSE].shift(1))
        df[TableColumn.EXP_MARKET] = df[TableColumn.MARKET].cumsum().apply(np.exp)
        df[TableColumn.EXP_MARKET][0] = 1

        df[TableColumn.DATE] = df[TableColumn.DATE].map(lambda x: Calculation.timeConvert(x))

        date = list(df[TableColumn.DATE].map(lambda x : str(x).split(" ")[0]))
        return date,list(df[TableColumn.EXP_MARKET].map(lambda x: round((x-1) * 100, 2))),df

    def getTrainData(asset_class,security):
        train_start=datetime(2011, 1, 1)
        train_end=datetime(2011, 6, 1)
        s,s1,train_df = Calculation.getMarketData(asset_class, security, train_start, train_end)

        return train_df

    def timeConvert(x):
        st = str(x).split(" ")[0].split('-')
        return datetime(int(st[0]), int(st[1]), int(st[2]))

    # dual thrust 趋势跟踪，日内交易，适用每分钟的数据，IntradayNYSEMS7/NYSE_
    # 突破BuyLine买进，突破SellLine卖出
    def DualThrust(response,data, days, K1=0.05, K2=0.01):
        data_res = pd.DataFrame()
        HH = max(data[TableColumn.HIGH])
        LC = min(data[TableColumn.CLOSE])
        HC = max(data[TableColumn.CLOSE])
        LL = min(data[TableColumn.LOW])
        # 获取 Range
        Range = max((HH - LC), (HC - LL))
        # 计算BuyLine 和 SellLine
        data_res['BuyLine'] = data[TableColumn.OPEN] + K1 * Range
        data_res['SellLine'] = data[TableColumn.OPEN] - K2 * Range
        data_res[TableColumn.REGIME] = np.where(data[TableColumn.CLOSE] < data_res['SellLine'], 1, 0)
        data_res[TableColumn.REGIME] = np.where(data[TableColumn.CLOSE] > data_res['BuyLine'], -1,
                                                data_res[TableColumn.REGIME])
        data_res[TableColumn.MARKET] = np.log(data[TableColumn.CLOSE] / data[TableColumn.CLOSE].shift(1))
        data_res[TableColumn.STRATEGY] = data_res[TableColumn.REGIME].shift(1) * data_res[TableColumn.MARKET]
        data_res[TableColumn.STRATEGY].fillna(0, inplace=True)
        data_res[TableColumn.MARKET].fillna(0, inplace=True)

        data_res[TableColumn.EXP_STRATEGY] = data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_MARKET] = data_res[TableColumn.MARKET].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        data_res[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        strategyName = Strategies.DualThrust
        regime = data_res[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))
        Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = Calculation.data_calculation(
            data_res, days)

        return response, strategyName, regime, Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio

    # 简单多均线择时，日间交易,适用每日交易的数据 ：FOREX_2011
    # 多头市场，当5日均值>10日>20>30,买进；
    # 空头市场，5日<10日<20日<30日，卖出
    # 当在多头市场，5日均线回落下叉（死叉）10日均线，卖出
    # 当空头排列后期，10日均线上升超过（金叉）20日均线，买入
    def SimpleMultiAverage(response,df, days):
        data_res = pd.DataFrame()
        mav_5 = df[TableColumn.CLOSE].ewm(span=5).mean()
        mav_10 = df[TableColumn.CLOSE].ewm(span=10).mean()
        mav_20 = df[TableColumn.CLOSE].ewm(span=20).mean()
        mav_30 = df[TableColumn.CLOSE].ewm(span=30).mean()
        data_res['mav_5'] = np.round(mav_5, 2)
        data_res['mav_10'] = np.round(mav_10, 2)
        data_res['mav_20'] = np.round(mav_20, 2)
        data_res['mav_30'] = np.round(mav_30, 2)

        data_res[TableColumn.REGIME] = np.where((data_res['mav_5'].shift() > data_res['mav_10'].shift()) &
                                                (data_res['mav_10'].shift() > data_res['mav_20'].shift()) &
                                                (data_res['mav_20'].shift() > data_res['mav_30'].shift()) &
                                                (data_res['mav_5'] < data_res['mav_10']), 1, 0)

        data_res[TableColumn.REGIME] = np.where((data_res['mav_5'] > data_res['mav_10']) &
                                                (data_res['mav_10'] > data_res['mav_20']) &
                                                (data_res['mav_20'] > data_res['mav_30']), -1,
                                                data_res[TableColumn.REGIME])

        data_res[TableColumn.REGIME] = np.where((data_res['mav_5'].shift() < data_res['mav_10'].shift()) &
                                                (data_res['mav_10'].shift() < data_res['mav_20'].shift()) &
                                                (data_res['mav_20'].shift() < data_res['mav_30'].shift()) &
                                                (data_res['mav_10'] > data_res['mav_20']), -1,
                                                data_res[TableColumn.REGIME])

        data_res[TableColumn.REGIME] = np.where((data_res['mav_5'] < data_res['mav_10']) &
                                                (data_res['mav_10'] < data_res['mav_20']) &
                                                (data_res['mav_20'] < data_res['mav_30']), 1,
                                                data_res[TableColumn.REGIME])

        data_res[TableColumn.MARKET] = np.log(df[TableColumn.CLOSE] / df[TableColumn.CLOSE].shift(1))
        data_res[TableColumn.STRATEGY] = data_res[TableColumn.REGIME].shift(1) * data_res[TableColumn.MARKET]
        data_res[TableColumn.STRATEGY].fillna(0, inplace=True)
        data_res[TableColumn.MARKET].fillna(0, inplace=True)
        data_res[TableColumn.EXP_STRATEGY] = data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_MARKET] = data_res[TableColumn.MARKET].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        data_res[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        strategyName = Strategies.SimpleMultiAverage
        regime = data_res[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))
        Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = Calculation.data_calculation(
            data_res, days)

        return response, strategyName, regime, Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio

    # KDJ随机指标
    # n日RSV=（Cn－Ln）/（Hn－Ln）×100
    # 公式中，Cn为第n日收盘价；Ln为n日内的最低价；Hn为n日内的最高价。
    # 其次，计算K值与D值：
    # 当日K值=2/3×前一日K值+1/3×当日RSV
    # 当日D值=2/3×前一日D值+1/3×当日K值
    # KDJ<20,金叉买入，K、J上升大于D
    # KDJ>80,死叉卖出,K、J下跌小于D
    def KDJ(response,df, days, n=9, m=2):
        data_res = pd.DataFrame()
        data_res["Min"] = (df[TableColumn.LOW].rolling(n)).mean()
        data_res["Max"] = (df[TableColumn.HIGH].rolling(n)).mean()
        data_res["rsv"] = (df[TableColumn.CLOSE] - data_res["Min"]) / (data_res["Max"] - data_res["Min"]) * 100
        data_res["K"] = data_res["rsv"].ewm(adjust=False, alpha=1 / (m + 1), ignore_na=True).mean()
        data_res["D"] = data_res["K"].ewm(adjust=False, alpha=1 / (m + 1), ignore_na=True).mean()
        data_res["J"] = 3 * data_res["K"] - 2 * data_res["D"]
        data_res.fillna(0, inplace=True)
        data_res[TableColumn.REGIME] = np.where((data_res["K"].shift(1) > data_res["D"].shift(1)) &
                                                (data_res["K"] <= data_res["D"]) &
                                                (data_res["J"].shift(1) > data_res["D"].shift(1)) &
                                                (data_res["J"] <= data_res["D"]), 1, 0)

        data_res[TableColumn.REGIME] = np.where((data_res["K"] > 80) &
                                                (data_res["D"] > 80) &
                                                (data_res["J"] > 80), 1, 0)

        data_res[TableColumn.REGIME] = np.where((data_res["K"].shift(1) <= data_res["D"].shift(1)) &
                                                (data_res["K"] > data_res["D"]) &
                                                (data_res["J"].shift(1) <= data_res["D"].shift(1)) &
                                                (data_res["J"] > data_res["D"]), -1, data_res[TableColumn.REGIME])

        data_res[TableColumn.REGIME] = np.where((data_res["K"] < 20) &
                                                (data_res["D"] < 20) &
                                                (data_res["J"] < 20), -1, data_res[TableColumn.REGIME])

        data_res[TableColumn.MARKET] = np.log(df[TableColumn.CLOSE] / df[TableColumn.CLOSE].shift(1))
        data_res[TableColumn.STRATEGY] = data_res[TableColumn.REGIME].shift(1) * data_res[TableColumn.MARKET]
        data_res[TableColumn.STRATEGY].fillna(0, inplace=True)
        data_res[TableColumn.MARKET].fillna(0, inplace=True)

        data_res[TableColumn.EXP_STRATEGY] = data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_MARKET] = data_res[TableColumn.MARKET].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        data_res[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        strategyName = Strategies.KDJ
        regime = data_res[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))
        Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = Calculation.data_calculation(
            data_res, days)

        return response, strategyName, regime, Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio

    def MACD(response,data, days, short_=12, long_=26, m=9):
        data_res = pd.DataFrame()
        data_res['diff'] = data[TableColumn.CLOSE].ewm(adjust=False, alpha=2 / (short_ + 1), ignore_na=True).mean() - \
                           data[TableColumn.CLOSE].ewm(adjust=False, alpha=2 / (long_ + 1), ignore_na=True).mean()

        data_res['dea'] = data_res['diff'].ewm(adjust=False, alpha=2 / (m + 1), ignore_na=True).mean()

        data_res['macd'] = 2 * (data_res['diff'] - data_res['dea'])
        data_res['cal_diff'] = data_res['diff'] - data_res['diff'].shift(1)
        data_res['cal_dea'] = data_res['dea'] - data_res['dea'].shift(1)
        data_res[TableColumn.REGIME] = np.where((data_res['cal_diff'] < 0) & (data_res['cal_dea'] < 0), 1, 0)
        data_res[TableColumn.REGIME] = np.where((data_res['cal_diff'] > 0) & (data_res['cal_dea'] > 0), -1,
                                                data_res[TableColumn.REGIME])
        data_res[TableColumn.MARKET] = np.log(data[TableColumn.CLOSE] / data[TableColumn.CLOSE].shift(1))
        data_res[TableColumn.STRATEGY] = data_res[TableColumn.REGIME].shift(1) * data_res[TableColumn.MARKET]

        data_res[TableColumn.STRATEGY].fillna(0, inplace=True)
        data_res[TableColumn.MARKET].fillna(0, inplace=True)

        data_res[TableColumn.EXP_STRATEGY] = data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)
        logging.info("data_res[TableColumn.STRATEGY]")
        # logging.info(data_res[TableColumn.STRATEGY])
        # #
        # logging.info("data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)")
        # logging.info(data_res[TableColumn.STRATEGY].cumsum().apply(np.exp))

        data_res[TableColumn.EXP_MARKET] = data_res[TableColumn.MARKET].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        data_res[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        strategyName = Strategies.MACD
        regime = data_res[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))

        Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = Calculation.data_calculation(
            data_res, days)

        return response, strategyName, regime, Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio

    # buy：
    # kama_{t}-kama_{t-1} > filter
    # and kama_{t-1}-kama_{t-2} > filter
    # sell：
    # kama_{t}-kama_{t-1} < -filter
    # and kama_{t-1}-kama_{t-2} < -filter
    def KAMA(response,df, days, thr=0.0002):
        data_res = pd.DataFrame()
        data_res['Change'] = np.abs(df[TableColumn.CLOSE] - df[TableColumn.CLOSE].shift(10))
        data_res['Volatility'] = np.abs(df[TableColumn.CLOSE] - df[TableColumn.CLOSE].shift(1)).rolling(10).sum()
        data_res['ER'] = data_res['Change'] / (data_res['Volatility']+0.0001)
        data_res['SC'] = (data_res['ER'] * (2 / (2 + 1) - 2 / (30 + 1)) + 2 / (30 + 1)) ** 2
        data_res['KAMA'] = df[TableColumn.CLOSE][0:10].mean()
        data_res['KAMA'] = data_res['KAMA'].shift(1) + data_res['SC'] * (
                df[TableColumn.CLOSE] - data_res['KAMA'].shift(1))
        data_res[TableColumn.REGIME] = 0
        data_res[TableColumn.REGIME] = np.where((((data_res['KAMA'] - data_res['KAMA'].shift(1)) > thr) & (
                (data_res['KAMA'].shift(1) - data_res['KAMA'].shift(2)) > thr)), 1, 0)
        data_res[TableColumn.REGIME] = np.where((((data_res['KAMA'] - data_res['KAMA'].shift(1)) < -thr) & (
                (data_res['KAMA'].shift(1) - data_res['KAMA'].shift(2)) < -thr)), -1, data_res[TableColumn.REGIME])
        data_res[TableColumn.MARKET] = np.log(df[TableColumn.CLOSE] / df[TableColumn.CLOSE].shift(1))
        data_res[TableColumn.STRATEGY] = data_res[TableColumn.REGIME].shift(1) * data_res[TableColumn.MARKET]
        data_res[TableColumn.STRATEGY].fillna(0, inplace=True)
        data_res[TableColumn.MARKET].fillna(0, inplace=True)


        data_res[TableColumn.EXP_STRATEGY] = data_res[TableColumn.STRATEGY].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_MARKET] = data_res[TableColumn.MARKET].cumsum().apply(np.exp)
        data_res[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        data_res[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        strategyName = Strategies.KAMA

        regime = data_res[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))

        Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio = Calculation.data_calculation(
            data_res, days)

        return response, strategyName, regime, Performance, Diff, Market, AnnualizedReturn, MaxDrawdown, Alpha, Beta, SharpeRatio

    def LogisticRegression(response,df, days,train_df):

        market = train_df.copy()
        # print(market)
        market.index = pd.to_datetime(market.index)
        market = market.sort_index(ascending=True)
        market['returns'] = market[TableColumn.CLOSE].pct_change()
        market.dropna(inplace=True)
        market["Min"] = (market[TableColumn.LOW].rolling(9)).mean()
        market["Max"] = (market[TableColumn.HIGH].rolling(9)).mean()
        market["rsv"] = (market[TableColumn.CLOSE] - market["Min"]) / (market["Max"] - market["Min"]) * 100
        market["K"] = market["rsv"].ewm(adjust=False, alpha=1 / (2 + 1), ignore_na=True).mean()
        market["D"] = market["K"].ewm(adjust=False, alpha=1 / (2 + 1), ignore_na=True).mean()
        market["J"] = 3 * market["K"] - 2 * market["D"]
        market.fillna(0, inplace=True)
        x_train = market[["K", "D", "J"]]
        x_train = sklearn.preprocessing.scale(x_train)
        lm = linear_model.LogisticRegression(penalty='l2', C=1.0, max_iter=100)
        y_train = np.sign(market[TableColumn.CLOSE].pct_change().shift(-1))
        y_train.replace(to_replace=np.NaN, value=0, inplace=True)
        y_train = y_train.values.reshape(-1, 1)
        lm.fit(x_train, y_train)
        market['prediction'] = lm.predict(x_train)
        market_test = df.copy()
        market_test.index = pd.to_datetime(market_test.index)
        market_test = market_test.sort_index(ascending=True)


        market_test['returns'] = market_test[TableColumn.CLOSE].pct_change()
        market_test.dropna(inplace=True)
        market_test["Min"] = (market_test[TableColumn.LOW].rolling(9)).mean()
        market_test["Max"] = (market_test[TableColumn.HIGH].rolling(9)).mean()
        market_test["rsv"] = (market_test[TableColumn.CLOSE] - market_test["Min"]) / (market_test["Max"] - market_test["Min"]) * 100
        market_test["K"] = market_test["rsv"].ewm(adjust=False, alpha=1 / (2 + 1), ignore_na=True).mean()
        market_test["D"] = market_test["K"].ewm(adjust=False, alpha=1 / (2 + 1), ignore_na=True).mean()
        market_test["J"] = 3 * market_test["K"] - 2 * market_test["D"]
        market_test.fillna(0, inplace=True)
        x_test = market_test[["K", "D", "J"]]
        x_test = sklearn.preprocessing.scale(x_test)
        y_test = np.sign(market_test[TableColumn.CLOSE].pct_change().shift(-1))
        y_test.replace(to_replace=np.NaN, value=0, inplace=True)


        # y_test = y_test.values.reshape(-1, 1)
        print(y_test.shape)
        market_test['prediction'] = lm.predict(x_test)
        market_test[TableColumn.MARKET] = np.log(market_test[TableColumn.CLOSE] / market_test[TableColumn.CLOSE].shift(1))
        market_test[TableColumn.STRATEGY] = (market_test['prediction'].shift(1) * market_test[TableColumn.MARKET])
        market_test[TableColumn.STRATEGY].fillna(0, inplace=True)
        market_test[TableColumn.MARKET].fillna(0, inplace=True)

        market_test[TableColumn.EXP_MARKET] = market_test[TableColumn.MARKET].cumsum().apply(np.exp)
        market_test[TableColumn.EXP_STRATEGY] = market_test[TableColumn.STRATEGY].cumsum().apply(np.exp)
        market_test[TableColumn.EXP_STRATEGY].fillna(1, inplace=True)
        market_test[TableColumn.EXP_MARKET].fillna(1, inplace=True)
        StrategyName = Strategies.LogisticRegression
        regime = market_test[TableColumn.EXP_STRATEGY].map(lambda x: round((x-1) * 100, 2))

        Performance,Diff,Market,AnnualizedReturn,MaxDrawdown,Alpha,Beta,SharpeRatio = Calculation.data_calculation(market_test, days)

        return response,StrategyName, regime, Performance,Diff,Market,AnnualizedReturn,MaxDrawdown,Alpha,Beta,SharpeRatio





        # sharpeRatio,annualReturns,annalMarket,beta,alpha,maxDrawdown
    def data_calculation(data_res, days):

        SharpeRatio = ((data_res[TableColumn.EXP_STRATEGY] - 1).mean() - 0.003) / (data_res[TableColumn.EXP_STRATEGY] - 1).std()
        AnnualizedReturn = (data_res[TableColumn.EXP_STRATEGY][-1] - 1)/ days * 252
        AnnualizedMarket = (data_res[TableColumn.EXP_MARKET][-1] - 1) / days * 252
        Beta = (np.cov((data_res[TableColumn.EXP_MARKET] - 1), (data_res[TableColumn.EXP_STRATEGY] - 1)))[0][
                   1] / np.var((data_res[TableColumn.EXP_MARKET] - 1))
        Alpha = (AnnualizedReturn - 0.003) - Beta * (AnnualizedMarket - 0.02)
        i = (1 - data_res[TableColumn.EXP_STRATEGY] / np.maximum.accumulate(
            data_res[TableColumn.EXP_STRATEGY])).idxmax()  # 结束位置
        if i == 0:
            MaxDrawdown = 0
            return AnnualizedReturn,MaxDrawdown,Alpha,Beta,SharpeRatio
        j = (data_res[TableColumn.EXP_STRATEGY][:i]).idxmax()  # 开始位置
        MaxDrawdown = (data_res[TableColumn.EXP_STRATEGY][i] / data_res[TableColumn.EXP_STRATEGY][j] - 1)
        Performance = data_res[TableColumn.EXP_STRATEGY][-1]
        Market = data_res[TableColumn.EXP_MARKET][-1]
        Diff = Performance -Market
        return round((Performance-1) * 100, 2),Diff,round((Market-1) * 100, 2),AnnualizedReturn,MaxDrawdown,Alpha,Beta,SharpeRatio


