from django.test import TestCase
import requests
import json
import logging

# Create your tests here.
class TestClass(TestCase):
    def setUp(self):
        print('>>Test setUp')

    def tearDown(self):
        print('>>Test tearDown')

    def test_demo(self):
        logging.info("test test_demo")
        json_data = {"startTime": "2011-01-02", "interval": "30", "modelFrequency": "day",
                               "tableProductData": [{"assetClass": "FOREX", "security": "AEDAUD"},
                                                    {"assetClass": "FOREX", "security": "JPYUSD"}],
                               "tableStrategyData": ["MACD", "KDJ"]}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        response = requests.post("http://127.0.0.1:8899/api/getResult", json=json_data, headers=headers)


        print("------------------------------------------------------------------------")
        data = json.loads(response.text)
        print(">>response.text:errorCode:{}\nerrorMessage:{}\nPerformance:{}\n"
              .format(data["error"]["code"],data["error"]['message'],data['data']['securityData'][0]['calcResult'][0]["Performance"]))
        print(">>response.url:{}".format(response.url))
        print(">>response.encoding:{}".format(response.encoding))
        print(">>response.status_code:{}".format(response.status_code))
