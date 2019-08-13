# Teamwork
Directories:

>  my-project : front end
>
>  my-site: back end

#### Run Vue

```
# go to my-project directory
cd /Teamwork/my-project

# run your vue project
npm run dev
```

#### Run Django Server

```
# go to mysite directory
cd /Teamwork/mysite (pycharm project terminal defaults this path)

# run your server
python manage.py runserver 0.0.0.0:8899
```

<br>

### 0. Standards

```json
{
  "error": {
    "code": ,
    "message": 
  },
  "data": {
    
  }
}
```

### 1. Get Security

> Description: Get specific securities from selected asset class

API:

```son
GET   http://192.168.43.141:8899/api/getSecurity
```

Parameter example:

```json
{
  "asset_class": "NASDAQ"
}
```

Return data:

```json
{
  "error": {
    "code": 0,
    "message": ""
  },
  "data": {
    "asset_class": "FOREX", 
    "security": [
      {"value": "AEDAUD", "label": "AEDAUD"}, 
      {"value": "AEDCAD", "label": "AEDCAD"}, 
      {"value": "AEDCHF", "label": "AEDCHF"}, 
      {"value": "AEDDKK", "label": "AEDDKK"}, 
      {"value": "AEDEUR", "label": "AEDEUR"}, 
      {"value": "AEDGBP", "label": "AEDGBP"}, 
      {"value": "AEDINR", "label": "AEDINR"}
    ]
  }
}
```

Return code:

```son
200 - OK
```

### 2. Submit configuration

> Description: After user's selection overall, submit data to back end
>
> 传递参数信息给后台，返回画图需要的数据
>

API:

```son
POST   http://192.168.43.141:8899/api/getResult
```

Parameter example:

```json
{
  "startTime": "2017-01-01",
  "endTime": "2017-12-01",
  "modelFrequency": "day",
  "tableProductData": [
    {
      "assetClass": "FOREX",
      "security": "GBPUSD"
    },
    {
      "assetClass": "NASDAQ",
      "security": "A"
    }
  ],
  "tableStrategyData": [
    {"strategy": "MACD"},
    {"strategy": "KDJ"}
  ]
}
```

Return data:

```json
{
  "securityData": [
    {
      "secName": "IBM",
      "date": ["2017-01-01", "2017-01-02", ..., "2017-06-01"],
      "marketData": ["10", "20", "30"],
      "calcResult": [
        {
          "stratName": "MACD",
          "regime": ["20", "30", "40"],
          "Yield": "12.03%",
          "Benchmark": "10.05%",
          "Sharpe Ratio": "0.089",
          "Alpha": "0.058",
          "Beta": "1.029",
          "Max Drawdown": "2.390"
      	},
        {
          "stratName": "KDJ",
          "regime": ["20", "30", "40"],
          "Yield": "12.03%",
          "Benchmark": "10.05%",
          "Sharpe Ratio": "0.089",
          "Alpha": "0.058",
          "Beta": "1.029",
          "Max Drawdown": "2.390"
        }
      ]
  	}
  ]
}
```

Return code:

```son
200 - OK
```

