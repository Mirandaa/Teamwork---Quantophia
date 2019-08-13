<template>
  <div id="app">

    <Menu mode="horizontal">
      <div @click="backhome()" class="title">
        <img src="./assets/logo.svg" class="logo">
      </div>
      <div @click="backhome()" class="title">Back Testing Tool</div>
    </Menu>

    <div class="layout">
        <Layout class="layout-center">
            <Content class="content-center">
                <Breadcrumb :style="{margin: '20px 0'}">
                    <BreadcrumbItem>Back Testing Configurations</BreadcrumbItem>
                </Breadcrumb>

                <Card>
                    <div class="config-selection">
                      <img src="./assets/time.svg" alt="">
                      <div class="selection-title">
                        Select Time
                      </div>
                      <Row class="picker">
                        <div class="picker-left">
                          From:
                        </div>
                        <Col span="12" class="picker-button">
                          <DatePicker type="date" v-model="startTime" placeholder="Select start date" :options="startTimeOption" @on-change="onStartTimeChange" class="picker-style"/>
                        </Col>
                        <div class="picker-left-to">
                          To:
                        </div>
                        <Col span="12" class="picker-button">
                          <DatePicker type="date" v-model="endTime" placeholder="Select end date" :options="endTimeOption" @on-change="onEndTimeChange" class="picker-style"/>
                        </Col>
                        <div class="picker-left2">
                          Frequency:
                        </div>
                        <Select class="picker-style picker-button " v-model="modelFrequency" clearable placeholder="Select frequency">
                          <Option v-for="item in frequencies" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                      </Row>
                    </div>

                    <div class="config-selection">
                      <img src="./assets/product.svg" alt="">
                      <div class="selection-title">
                        Select 1/n financial product(s)
                      </div>
                      <Row class="picker">
                        <div class="picker-left">
                          Asset Class:
                        </div>
                        <Select class="picker-button" v-model="modelProduct" clearable placeholder="Select asset class" @on-change="getSecurityData()">
                          <Option v-for="item in assetClass" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <div class="picker-left2">
                          Security:
                        </div>
                        <Select filterable class="picker-button" v-model="modelSecurity" clearable placeholder="Select security">
                          <Option v-for="item in security" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <Button type="primary" ghost class="add-button" @click="addProduct" :disabled="!modelProduct || !modelSecurity">Add</Button>
                      </Row>
                      <Table stripe border :columns="productColumns" :data="tableProductData" class="data-table">
                        <template slot-scope="{ row }" slot="assetClass">
                          <strong>{{ row.assetClass }}</strong>
                        </template>
                        <template slot-scope=" {row, index} " slot="action">
                          <Button type="error" size="small" @click="removeProduct(index)">Delete</Button>
                        </template>
                      </Table>
                    </div>

                    <div class="config-selection">
                      <img src="./assets/strategy.svg" alt="" class="strategy">
                      <div class="selection-title">
                        Select 1/n strategy(s)
                      </div>
                      <Row class="picker">
                        <div class="picker-left">
                          Strategy:
                        </div>
                        <Select class="picker-button" v-model="modelStrategy" clearable placeholder="Select strategy">
                          <Option v-for="item in strategy" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <Button type="primary" ghost class="add-button" @click="addStrategy" :disabled="!modelStrategy">Add</Button>
                      </Row>
                      <Table stripe border :columns="strategyColumns" :data="tableStrategyData" class="data-table">
                        <template slot-scope="{ row }" slot="strategy">
                          <strong>{{ row.strategy }}</strong>
                        </template>
                        <template slot-scope=" {row, index} " slot="action">
                          <Button type="error" size="small" @click="removeStrategy(index)">Delete</Button>
                        </template>
                      </Table>
                      <Button type="primary" class="submit-button" @click="submitData()" :disabled="!startTime || !endTime || !modelFrequency || tableProductData.length == 0 || tableStrategyData.length == 0">Submit</Button>
                    </div>
                </Card>
            </Content>

            <!-- 这里是提交设置之后生成图表-->
            <Content class="content-center">
                <Breadcrumb :style="{margin: '20px 0'}">
                    <BreadcrumbItem>Result Overview</BreadcrumbItem>
                </Breadcrumb>

                <Card>
                    <div class="config-selection">


                      <router-view v-if="isRouterAlive"/>
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2019 &copy; belongs to original authors<br>
              <div>
              Programmed By : Maggie | Davis | Sue | Sophy
              </div>
            </Footer>
        </Layout>
    </div>
  </div>
</template>

<script>
let moment = require("moment")

export default {
  provide() {
    return {
      reload: this.reload
    }
  },

  data() {
    return {
      isRouterAlive: true,
      startTime: '',
      endTime: '',
      startTimeOption: {},
      endTimeOption: {},
      frequencies: [
        {
          value: 'day',
          label: 'day'
        },
        {
          value: 'minute',
          label: 'minute'
        }
      ],
      assetClass: [
        {
          value: 'FOREX',
          label: 'FOREX'
        },
        {
          value: 'IntradayNYSEMS7',
          label: 'IntradayNYSEMS7'
        },
        {
          value: 'LIFFE_FuturesOptions',
          label: 'LIFFE_FuturesOptions',
        },
        {
          value: 'NASDAQ',
          label: 'NASDAQ'
        }
      ],
      security: [],
      securityItem: {
        value: '',
        label: ''
      },
      strategy: [
        {
          value: 'MACD',
          label: 'MACD'
        },
        {
          value: 'KAMA',
          label: 'KAMA'
        },
        {
          value: 'KDJ',
          label: 'KDJ'
        }
      ],
      modelFrequency: '',
      modelProduct: '',
      modelSecurity: '',
      modelStrategy: '',
      productColumns: [
        {
          title: 'Asset Class',
          key: 'assetClass',
        },
        {
          title: 'Security',
          key: 'security'
        },
        {
          title: 'Action',
          slot: 'action',
          align: 'center'
        }
      ],
      strategyColumns: [
        {
          title: 'Trading Strategy',
          key: 'strategy'
        },
        {
          title: 'Action',
          slot: 'action',
          align: 'center'
        }
      ],
      
      tableProductData: [],
      securityList: [],
      tableStrategyData: [],
      strategyList: [],
      tableReturnData: [],
      //  Test return to Chart.vue of chart data
      testChartData: [
        {
          secName: "IBM",
          date: ['2009-12-31', '2010-01-04', '2010-01-05', '2010-01-06',
                 '2010-01-07', '2010-01-08', '2010-01-11', '2010-01-12',
                 '2010-01-13', '2010-01-14', '2013-01-11', '2013-01-14', 
                 '2013-01-15', '2013-01-16', '2013-01-17', '2013-01-18', 
                 '2013-01-22', '2013-01-23', '2013-01-24', '2013-01-25'],
          marketData: [22.625179290771484, 22.3319034576416, 22.174535751342773, 22.045780181884766, 
          22.06723976135254, 22.21030044555664, 21.924177169799805, 22.017168045043945, 
          22.346208572387695, 22.432044982910156, 22.052932739257812, 21.93848419189453, 
          22.253219604492188, 21.709585189819336, 21.20886993408203, 21.101573944091797, 
          20.951358795166016, 21.008583068847656, 20.865522384643555, 20.97281837463379],
          calcResult: [
            {
              stratName: "MACD",
              regime: [22.389127731323242, 22.145923614501953, 22.06723976135254, 22.038625717163086, 
          22.03147315979004, 22.045780181884766, 21.781116485595703, 21.952789306640625, 
          22.281831741333008, 21.766809463500977, 22.03147315979004, 21.90987205505371, 
          21.831188201904297, 20.865522384643555, 21.06580924987793, 20.951358795166016, 
          20.865522384643555, 20.522174835205078, 20.050071716308594, 20.836910247802734],
              Yield: "12.03%",
              Benchmark: "10.05%",
              SharpeRatio: "0.089",
              Alpha: "0.058",
              Beta: "1.029",
              MaxDrawdown: "2.390"
           },
            {
              stratName: "KDJ",
              regime: [22.45350456237793, 22.324748992919922, 22.06723976135254, 22.017168045043945, 
            21.917024612426758, 22.08869743347168, 21.859800338745117, 21.795421600341797, 
            21.881258010864258, 22.3319034576416, 21.716737747192383, 21.838340759277344, 
            22.174535751342773, 21.709585189819336, 21.044349670410156, 21.008583068847656, 
            20.886981964111328, 20.836910247802734, 20.69384765625, 20.1430606842041],
              Yield: "14.13%",
              Benchmark: "9.09%",
              SharpeRatio: "0.123",
              Alpha: "1.238",
              Beta: "0.893",
              MaxDrawdown: "1.888"
            }
         ]
       }
     ]
    }
  },
  mounted() {
    this.onStartTimeChange(this.startTime)
    this.onEndTimeChange(this.endTime)
  },
  methods: {
    /*
         * Triggered when the start time changes, setting the date when the end time is not selectable
         * end time >= start time & end time <= Date.now()
         * @param {string} startTime : Formatted date
         * @param {string} type : Current date type
    */
    onStartTimeChange(startTime, type) {
      this.endTimeOption = {
        disabledDate(endTime) {
          return endTime < new Date(startTime) || endTime > Date.now()
        }
      }
    },
    /*
         * Triggered when the end time changes, setting the date when the start time cannot be selected
         * start time <= end time & start time <= Date.now()
         * @param {string} date : Formatted date
         * @param {string} type : Current date type
    */
    onEndTimeChange(endTime, type) {
      this.startTimeOption = {
        disabledDate(startTime) {
          return startTime > new Date(endTime) || startTime > Date.now()
        }
      }
    },

    addProduct() {
      var flag = true

      for (var i = 0; i < this.securityList.length; i++) {
        if (this.modelSecurity == this.securityList[i]) {
          alert('Already add this product!\nPlease choose another security.')
          this.modelSecurity = ''
          flag = false
        }
      }

      if (flag) {
        this.tableProductData.push({assetClass: this.modelProduct, security: this.modelSecurity})
        this.securityList.push(this.modelSecurity)
        console.log(this.tableProductData)
        this.modelProduct = ''
        this.modelSecurity = ''
      }
    },

    removeProduct(index) {
      this.tableProductData.splice(index, 1)
      this.securityList.splice(index, 1)
    },

    addStrategy() {
      var flag = true

      for (var i = 0; i < this.strategyList.length; i++) {
        if (this.modelStrategy == this.strategyList[i]) {
          alert('Already add this strategy!\nPlease choose another one.')
          this.modelStrategy = ''
          flag = false
        }
      }

      if (flag) {
        this.tableStrategyData.push({strategy: this.modelStrategy})
        this.strategyList.push(this.modelStrategy)
        console.log(this.tableStrategyData)
        this.modelStrategy = ''
      }
    },

    removeStrategy(index) {
      this.tableStrategyData.splice(index, 1)
      this.strategyList.splice(index, 1)
    },

    getSecurityData() {
      // get securties data from asset class
      let that = this
      console.log('select asset class: ' + '/getSecurity')
      this.axios({
        method: 'get',
        url: '/getSecurity',
        // timeout: 1000000 * 60 * 2,
        params: {
          asset_class: this.modelProduct
        }
      })
      .then(function (response) {
        that.security = response.data.data.security
      }).catch(function (error) {
        console.log(error)
      })
    },

    submitData() {
      // submit all data to backend
      let that = this
      console.log('click submit button and post:' + '/getResult')
      this.axios({
        method: 'post',
        url: '/getResult',
        data: {
          startTime: moment(this.startTime).format('YYYY-MM-DD'),
          endTime: moment(this.endTime).format('YYYY-MM-DD'),
          modelFrequency: this.modelFrequency,
          tableProductData: this.tableProductData,
          tableStrategyData: this.tableStrategyData
        }
      })
      .then(function (response) {
        that.tableReturnData = response.data.data.securityData
        console.log(response.data)
      }).catch(function (error) {
        console.log(error)
      })
      // this.$router.push({ path: '/Chart', query: { allData: this.tableReturnData}})
      this.$router.push({ path: '/Chart', query: { allData: this.testChartData}})
    },

    backhome() {
      this.$router.push('/')
    },

    reload() {
      this.isRouterAlive = false
      this.$nextTick(function() {
        this.isRouterAlive = true
      })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.wrapper {
  width: 500px;
  height: 400px;
}

.title{
  float: left;
  margin-left: 20px;
  font-size: 24px;
  cursor: pointer;
}

.logo{
  margin-top: 5px;
  margin-left: 20px;
  width: 50px;
  height: 50px;
}

.layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
}

.layout-center{
  display: block;
}

.content-center{
  padding: 0 50px;
}

.config-selection{
  text-align: left;
  margin: 10px 30px;
  border-bottom: solid #e8eaec 1px;

}

.config-selection img{
  width: 30px;
  height: auto;
  vertical-align: middle;
}

.config-selection img.strategy{
  width: 30px;
  height: 31px;
  vertical-align: middle;
}

.config-selection .selection-title{
  display: inline-flex;
  margin-left: 10px;
}

.picker{
  margin: 15px 0;
}

.picker .picker-style {
  width: 200px;
}

.picker .picker-left{
  float: left;
  vertical-align: middle;
  margin: 5px 0;
}

.picker .picker-left-to{
  float: left;
  vertical-align: middle;
  margin: 5px 0 5px 15px;
}

.picker .picker-left2{
  display: inline-table;
  vertical-align: middle;
  margin: 5px 0 5px 15px;
}

.picker .picker-button{
  margin-left: 15px;
  width: 200px;
}

.add-button{
  margin-left: 15px;
}

.data-table{
  margin-bottom: 20px;
}

.submit-button{
  margin-left: 93%;
  margin-bottom: 20px
}

.layout-footer-center{
    text-align: center;
}

.chart{
  padding: 20px;
  border-radius: 20px;
}

.chart h2 {
  margin-top: 0;
  padding: 10px 0 20px 0;
  color: #2c3e50;
}
</style>
