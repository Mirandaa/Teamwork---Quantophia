import pandas as pd
import pymysql
import logging
import time;
from sqlalchemy import create_engine
from polls.empty.constants import Constants,TableColumn
# import pandas_datareader.data as web

import datetime

# start = datetime.datetime(2010, 1, 1)
#
# end = datetime.datetime(2013, 1, 27)

# f = web.DataReader('A', 'yahoo', start, end)
# f.head()
pymysql.install_as_MySQLdb()
class LoadData:
    def LoadAllDataFrames(asset_class, security, start, end):
        logging.info('LoadAllDataFrames() method running  time: ' + str(time.asctime(time.localtime(time.time()))))

        engine = create_engine(Constants.SQLCONNECT)
        sql = Constants().getSQL(asset_class, security, start, end)
        print(sql)
        data = pd.read_sql(sql, con=engine)
        data.reset_index()

        data.index = data[TableColumn.DATE]

        logging.info('LoadAllDataFrames over.  time: ' + str(time.asctime(time.localtime(time.time()))))
        return data