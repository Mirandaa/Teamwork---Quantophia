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
    "code": 1,
    "message": "Get security success"
  },
  "data": {
    ['AACC', 'AAME', 'AAON', 'AAPL', 'AAWW', 'AAXJ', 'ABAX', 'ABCB', 'ABCD', 'ABCO', 'ABFS', 'ABIO', 'ABMD', 'ABTL', 'ACAD', 'ACAS', 'ACAT', 'ACCL', 'ACET', 'ACFC', 'ACFN', 'ACGL', 'ACHN', 'ACIW', 'ACLS', 'ACNB', 'ACOR', 'ACPW', 'ACTG', 'ACTS', 'ACUR', 'ACWI', 'ACWX', 'ACXM', 'ADAT', 'ADBE', 'ADEP', 'ADES', 'ADI', 'ADP', 'ADRA', 'ADRD', 'ADRE', 'ADRU', 'ADSK', 'ADTN', 'ADUS', 'ADVS', 'AEGR']
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
> 暂定：传递参数信息给后台，返回画图需要的数据:
>
> http://149.28.47.146:8899/api/configuration

API:

```son
POST   http://192.168.43.141:8899/api/submitConfig
```

Parameter example:

```json
{
  pending
}
```

Return data:

```json
{
  pending
}
```

Return code:

```son
200 - OK
```

###

