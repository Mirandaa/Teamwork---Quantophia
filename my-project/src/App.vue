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
                          <Radio label='360'>
                              <span>1Y</span>
                          </Radio>
                          <Radio label='720'>
                              <span>2Y</span>
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
                          Source:
                        </div>
                        <Select transfer="true" class="picker-button" placement="top-start" v-model="modelProduct" clearable filterable placeholder="Source" @on-change="getSecurityData()">
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
          title: 'Source',
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
      tableReturnData: []
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
      console.log('select source: ' + '/getSecurity')
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
