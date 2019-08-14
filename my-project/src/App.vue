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
                <Breadcrumb class="card-title">
                    <BreadcrumbItem>Back Testing Configurations</BreadcrumbItem>
                </Breadcrumb>

                <Card>
                  <div style="overflow: hidden;">
                    <div class="config-selection1">
                      <Icon type="md-time" size="24"/>
                      <div class="selection-title">
                        Select Time
                      </div>
                      <Row class="picker">
                        <div class="picker-left">
                          Start:
                        </div>
                        <Col span="12" class="picker-button">
                          <DatePicker transfer="true" type="date" placement="top-start" v-model="startTime" placeholder="Start date" :options="startTimeOption" @on-change="onStartTimeChange" class="picker-style"/>
                        </Col>
                        <RadioGroup v-model="interval" class="picker-left2">
                          <Radio label='30'>
                              <span>1M</span>
                          </Radio>
                          <Radio label='90'>
                              <span>3M</span>
                          </Radio>
                          <Radio label='180'>
                              <span>6M</span>
                          </Radio>
                          <Radio label='270'>
                              <span>9M</span>
                          </Radio>
                          <Radio label='360'>
                              <span>12M</span>
                          </Radio>
                        </RadioGroup>
                      </Row>
                    </div>

                    <div class="config-selection2">
                      <Icon type="md-done-all" size="24"/>
                      <div class="selection-title">
                        Select 1/n financial product(s)
                      </div>
                      <Row class="picker">
                        <div class="picker-left">
                          Asset Class:
                        </div>
                        <Select transfer="true" class="picker-button" placement="top-start" v-model="modelProduct" clearable filterable placeholder="Asset class" @on-change="getSecurityData()">
                          <Option v-for="item in assetClass" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <div class="picker-left2">
                          Security:
                        </div>
                        <Select filterable class="picker-button" placement="top-start" transfer="true" v-model="modelSecurity" clearable placeholder="Security">
                          <Option v-for="item in security" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <Button type="primary" ghost class="add-button" @click="addProduct" :disabled="!modelProduct || !modelSecurity">Add</Button>
                      </Row>

                    </div>

                    <div class="config-selection3">
                      <Row class="picker-strategy">
                        <div class="check-strategy">
                          <Checkbox
                          :indeterminate="indeterminate"
                          :value="checkAll"
                          @click.prevent.native="handleCheckAll" class="check-box">Select all strategies</Checkbox>
                        </div>
                        <CheckboxGroup v-model="checkAllGroup" @on-change="checkAllGroupChange">
                          <Checkbox class="check-box-label" label="MACD"></Checkbox>
                          <Checkbox class="check-box-label" label="KDJ"></Checkbox>
                          <Checkbox class="check-box-label" label="KAMA"></Checkbox>
                          <Checkbox class="check-box-label" label="LR"></Checkbox>
                          <Checkbox class="check-box-label" label="SMA"></Checkbox>
                          <Checkbox class="check-box-label" label="DT"></Checkbox>
                        </CheckboxGroup>
                      </Row>
                    </div>

                      <Table stripe border size="small" no-data-text="No data" :columns="productColumns" :data="tableProductData" class="data-table">
                        <template slot-scope="{ row }" slot="assetClass">
                          <strong>{{ row.assetClass }}</strong>
                        </template>
                        <template slot-scope=" {row, index} " slot="action">
                          <Button type="error" size="small" @click="removeProduct(index)">Delete</Button>
                        </template>
                      </Table>
                    
                    <div class="submit-button-line">
                      <Button type="primary" class="submit-button" @click="submitData()" :disabled="!startTime || !interval || tableProductData.length == 0 || checkAllGroup.length == 0">Submit</Button>
                    </div>

                    <Breadcrumb class="result-title">
                      <Icon type="md-pulse" size="24" class="result-icon"/>
                      <BreadcrumbItem>Result Overview</BreadcrumbItem>
                    </Breadcrumb>

                    <div class="config-selection">
                      <router-view v-if="isRouterAlive"/>
                    </div>
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
      startTime: '2011-01-01',
      endTime: '',
      startTimeOption: {},
      endTimeOption: {},
      interval: '30',
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
      indeterminate: false,
      checkAll: true,
      checkAllGroup: ['MACD', 'KDJ', 'KAMA', 'LR', 'SMA', 'DT'],
      modelProduct: '',
      modelSecurity: '',
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
      tableProductData: [],
      securityList: [],
      tableStrategyData: [],
      tableReturnData: [],
      //  Test return to Chart.vue of chart data
      testChartData1: [
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
      ],

      test1toN: [
        {
          secName: "AEDAUD",
          date: [
                  "2011-01-03",
                  "2011-01-04",
                  "2011-01-05",
                  "2011-01-06",
                  "2011-01-07",
                  "2011-01-08",
                  "2011-01-10",
                  "2011-01-11",
                  "2011-01-12",
                  "2011-01-13",
                  "2011-01-14",
                  "2011-01-15",
                  "2011-01-17",
                  "2011-01-18",
                  "2011-01-19",
                  "2011-01-20",
                  "2011-01-21",
                  "2011-01-22",
                  "2011-01-24",
                  "2011-01-25",
                  "2011-01-26",
                  "2011-01-27",
                  "2011-01-28",
                  "2011-01-29",
                  "2011-01-31"
          ],
          marketData: [
                  1.0,
                  1.011989509179468,
                  1.0206069689022106,
                  1.0228550018733609,
                  1.026227051330086,
                  1.0236043461970774,
                  1.026227051330086,
                  1.0348445110528288,
                  1.0236043461970776,
                  1.0232296740352191,
                  1.026227051330086,
                  1.0310977894342448,
                  1.029224428624953,
                  1.0247283626826527,
                  1.019108280254777,
                  1.0337204945672533,
                  1.03222180591982,
                  1.0299737729486695,
                  1.0228550018733606,
                  1.0228550018733606,
                  1.0236043461970774,
                  1.025103034844511,
                  1.0284750843012365,
                  1.0277257399775197,
                  1.0266017234919447
          ],
          calcResult: [
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
                    0.976923889372137,
                    0.976923889372137
              ],
              Performance: "97.69%",
              Market: "-4.97%",
              Diff: "102.66%",
              AnnualizedReturn: "-0.27%",
              MaxDrawdown: -0.034,
              Alpha: -0.018,
              Beta: -0.756,
              SharpeRatio: -4.392
            },
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
                  1.012748266321497,
                  1.0116406305945689
              ],
              Performance: "101.16%",
              Market: "-1.5%",
              Diff: "102.66%",
              AnnualizedReturn: "0.14%",
              MaxDrawdown: -0.022,
              Alpha: -0.003,
              Beta: -0.088,
              SharpeRatio: -0.54
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

    handleCheckAll () {
      if (this.indeterminate) {
        this.checkAll = false
      } else {
        this.checkAll = !this.checkAll
      }
      this.indeterminate = false

      if (this.checkAll) {
        this.checkAllGroup = ['MACD', 'KDJ', 'KAMA', 'LR', 'SMA', 'DT']
      } else {
        this.checkAllGroup = []
      }
    },

    checkAllGroupChange (data) {
      if (data.length === 6) {
        this.indeterminate = false
        this.checkAll = true
      } else if (data.length > 0) {
        this.indeterminate = true
        this.checkAll = false
      } else {
        this.indeterminate = false
        this.checkAll = false
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

    async submitData() {
      // submit all data to backend
      let that = this
      console.log('click submit button and post:' + '/getResult')
      await this.axios({
        method: 'post',
        url: '/getResult',
        data: {
          startTime: moment(this.startTime).format('YYYY-MM-DD'),
          interval: this.interval,
          tableProductData: this.tableProductData,
          tableStrategyData: this.checkAllGroup
        }
      })
      .then(function (response) {
        console.log(response.data.data.securityData)
        console.log(response.status)
        that.tableReturnData = response.data.data.securityData
      }).catch(function (error) {
        console.log(error)
      })

      // this.$router.push({ path: '/Chart', query: { allData: this.tableReturnData}})
      // this.$router.push({ path: '/Chart', query: { allData: this.testChartData1}})
      // test 1-n
      this.$router.push({ path: '/Chart', query: { allData: this.test1toN}})
      // test n-1
      // this.$router.push({ path: '/Chart', query: { allData: this.testNto1}})
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
  padding: 0 20px;
}

.card-title{
  margin: 12px 0;
}

.result-title{
  text-align: left;
  border-bottom: 1px solid #e9e9e9;
  padding-bottom: 5px;
}

.result-icon{
  color: #5c6b77;
  margin: 0 5px;
}

.config-selection{
  float: left;
  width: 100%;
  text-align: left;
  margin: 10px 10px;
}

.config-selection1{
  float: left;
  width: 34%;
  text-align: left;
}

.config-selection2{
  float: left;
  width: 38%;
  text-align: left;
}

.config-selection3{
  float: left;
  width: 28%;
  text-align: left;
}

.config-selection1 img{
  width: auto;
  height: 25px;
  vertical-align: middle;
}

.config-selection2 img{
  width: auto;
  height: 25px;
  vertical-align: middle;
}

.config-selection3 img.strategy{
  width: 24px;
  height: 25px;
  vertical-align: middle;
}

.selection-title{
  display: inline-flex;
  margin-left: 10px;
}

.picker{
  margin: 10px 0;
}

.picker .picker-style{
  width: 110px;
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
  margin: 5px 0 5px 8px;
}

.picker .picker-button{
  margin-left: 5px;
  width: 110px;
}

.picker-strategy{
  margin: 10px 0;
}

.add-button{
  margin-left: 5px;
}

.check-strategy{
  border-bottom: 1px solid #e9e9e9;
  padding-bottom:6px;
  margin-bottom:8px;
}

.check-box{
  font-size: 14px;
}

.check-box-label{
  margin-right: 6px;
}

.data-table{
  margin-bottom: 10px;
}

.submit-button-line{
  width: 100%;
  height: 14px;
}

.submit-button{
  float: right;
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



