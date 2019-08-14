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
          secName: "GBPUSD",
          date: [
                "2011-01-02",
                "2011-01-03",
                "2011-01-04",
                "2011-01-05",
                "2011-01-06",
                "2011-01-07",
                "2011-01-08",
                "2011-01-09",
                "2011-01-10",
                "2011-01-11",
                "2011-01-12",
                "2011-01-13",
                "2011-01-14",
                "2011-01-15",
                "2011-01-16",
                "2011-01-17",
                "2011-01-18",
                "2011-01-19",
                "2011-01-20",
                "2011-01-21",
                "2011-01-22"
          ],
          marketData: [
                0.0,
                0.9944758478931142,
                1.0020554984583763,
                0.995953237410072,
                0.9929342240493321,
                0.9985226104830421,
                0.9985226104830421,
                0.9983941418293936,
                1.0012204522096608,
                1.0025693730729703,
                1.0113694758478933,
                1.0175359712230216,
                1.0195272353545735,
                1.0195272353545735,
                1.0197841726618704,
                1.0210688591983554,
                1.024730215827338,
                1.0258864337101745,
                1.0218396711202467,
                1.0279419321685508,
                1.0279419321685508
          ],
          calcResult: [
              {
                  stratName: "MACD",
                  regime: [
                      1.0,
                      1.0,
                      0.9915565345080763,
                      0.9893772893772893,
                      0.9861263234757212,
                      0.9886530014641289,
                      0.9861263234757213,
                      0.9779145546705286,
                      0.9886530014641288,
                      0.9886530014641288,
                      0.9886530014641288,
                      0.9839827656287241,
                      0.9857737790354019,
                      0.9900989290713889,
                      0.9900989290713889,
                      1.0042952004808683,
                      1.005753342332746,
                      1.0079485115048075,
                      1.0079485115048075,
                      1.0079485115048075,
                      1.0086869353227597,
                      1.0101637829586643,
                      1.0134866901394495,
                      1.012748266321497
                  ],
                  Yield: "0.14%",
                  Benchmark: "0.31%",
                  SharpeRatio: -0.607,
                  Alpha: -0.004,
                  Beta: -0.114,
                  MaxDrawdown: "-2.21%"
              },
              {
                  stratName: "KDJ",
                  regime: [
                      1.0,
                      0.9881525360977416,
                      0.9798091042584435,
                      0.9776556776556775,
                      0.9744432274552758,
                      0.9769399707174232,
                      0.9744432274552759,
                      0.9663287472845764,
                      0.9769399707174231,
                      0.9765823792200888,
                      0.9765823792200888,
                      0.9765823792200888,
                      0.9783599226842681,
                      0.9740860533460042,
                      0.9740860533460042,
                      0.9740860533460042,
                      0.9740860533460042,
                      0.9762121051175853,
                      0.9762121051175853,
                      0.9762121051175853,
                      0.9762121051175853,
                      0.9762121051175853,
                      0.9762121051175853,
                      0.976923889372137
                  ],
                  Yield: "-0.26%",
                  Benchmark: "0.31%",
                  SharpeRatio: -4.297,
                  Alpha: -0.018,
                  Beta: -0.759,
                  MaxDrawdown: "-3.37%"
              }
          ]
        },
        {
          secName: "JPYUSD",
          date: [
                "2011-01-02",
                "2011-01-03",
                "2011-01-04",
                "2011-01-05",
                "2011-01-06",
                "2011-01-07",
                "2011-01-08",
                "2011-01-09",
                "2011-01-10",
                "2011-01-11",
                "2011-01-12",
                "2011-01-13",
                "2011-01-14",
                "2011-01-15",
                "2011-01-16",
                "2011-01-17",
                "2011-01-18",
                "2011-01-19",
                "2011-01-20",
                "2011-01-21",
                "2011-01-22"
          ],
          marketData: [
                0.0,
                0.9918699186991871,
                0.9918699186991871,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.9756097560975611,
                0.983739837398374,
                0.983739837398374,
                0.9756097560975611,
                0.983739837398374,
                0.9918699186991872,
                0.9756097560975612,
                0.9756097560975612,
                0.9837398373983741
          ],
          calcResult: [
              {
                  stratName: "MACD",
                  regime: [
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0,
                      1.0083333333333333,
                      1.0083333333333333,
                      1.0000683060109288,
                      1.0167361111111108,
                      1.0167361111111108,
                      1.0167361111111108,
                      1.0167361111111108,
                      1.0167361111111108,
                      1.0167361111111108,
                      1.025208912037037,
                      1.025208912037037,
                      1.016805560299028
                  ],
                  Yield: "0.19%",
                  Benchmark: "0.0%",
                  SharpeRatio: 0.45,
                  Alpha: 0.003,
                  Beta: 0.186,
                  MaxDrawdown: "-0.82%"
              },
              {
                  stratName: "KDJ",
                  regime: [
                      1.0,
                      1.0,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.0166666666666666,
                      1.025068870523416,
                      1.0082644628099175,
                      1.0082644628099175,
                      1.0082644628099175,
                      1.0082644628099175,
                      1.0082644628099175,
                      1.0082644628099175,
                      1.0166666666666668,
                      1.0166666666666668,
                      1.0166666666666668
                  ],
                  Yield: "0.19%",
                  Benchmark: "0.0%",
                  SharpeRatio: 1.867,
                  Alpha: -0.008,
                  Beta: -0.333,
                  MaxDrawdown: "-1.64%"
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
        console.log(response.data.data.securityData)
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



