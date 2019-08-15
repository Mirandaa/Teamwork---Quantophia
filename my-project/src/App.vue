<template>
  <div id="app">

    <Menu mode="horizontal">
      <div @click="backhome()" class="title">
        <img src="./assets/logo.svg" class="logo">
      </div>
      <div @click="backhome()" class="title">Quantophia</div>
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
                      <Button type="error" class="submit-button" @click="backhome()" :disabled="!startTime || !interval || tableProductData.length == 0 || checkAllGroup.length == 0">Reset</Button>
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
      startTime: '2011-06-01',
      endTime: '',
      startTimeOption: {},
      endTimeOption: {},
      interval: '180',
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
      indeterminate: true,
      checkAll: false,
      checkAllGroup: ['MACD', 'KDJ', 'LR'],
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
      ],

      testNto1: [
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
        },
        {
          secName: "JPYUSD",
          date: [
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
                "2011-01-22",
                "2011-01-24",
                "2011-01-25",
                "2011-01-26",
                "2011-01-27",
                "2011-01-28",
                "2011-01-29",
                "2011-01-30",
                "2011-01-31"
          ],
          marketData: [
                1.0,
                1.0,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9836065573770492,
                0.9918032786885246,
                0.9918032786885246,
                0.9836065573770492,
                0.9918032786885246,
                1.0000000000000002,
                0.9836065573770493,
                0.9836065573770493,
                0.9918032786885247,
                0.9918032786885247,
                0.9918032786885247,
                0.9918032786885247,
                0.9836065573770493,
                0.9918032786885247,
                1.0000000000000002,
                1.0000000000000002,
                0.9918032786885248
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
                    1.016805560299028,
                    1.016805560299028,
                    1.0252089120370367
              ],
              Performance: "102.52%",
              Market: "3.34%",
              Diff: "99.18%",
              AnnualizedReturn: "0.3%",
              MaxDrawdown: -0.008,
              Alpha: 0.006,
              Beta: 0.31,
              SharpeRatio: 0.533
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
      let that = this
      console.log('select asset class: ' + '/getSecurity')
      this.axios({
        method: 'get',
        url: '/getSecurity',
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
      let that = this
      console.log('click submit button and post:' + '/getResult')
      this.$Spin.show()

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

      this.$Spin.hide()
      this.$router.push({ path: '/Chart', query: { allData: this.tableReturnData}})
    },

    backhome() {
      this.$router.go(0)
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
