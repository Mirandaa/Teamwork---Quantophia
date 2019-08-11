<template>
  <div id="app">

    <Menu mode="horizontal">
      <div class="title">
        <img src="./assets/logo.svg" class="logo">
      </div>
      <div class="title">Back Testing Tool</div>
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
                        <Select class="picker-button" v-model="modelProduct" clearable placeholder="Select asset class">
                          <Option v-for="item in assetClass" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <div class="picker-left2">
                          Security:
                        </div>
                        <Select class="picker-button" v-model="modelSecurity" clearable placeholder="Select security" @on-open-change="getSecurityData()">
                          <Option v-for="item in security" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                        <Button type="primary" ghost class="add-button" @click="addProduct">Add</Button>
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
                        <Button type="primary" ghost class="add-button" @click="addStrategy">Add</Button>
                      </Row>
                      <Table stripe border :columns="strategyColumns" :data="tableStrategyData" class="data-table">
                        <template slot-scope="{ row }" slot="strategy">
                          <strong>{{ row.strategy }}</strong>
                        </template>
                        <template slot-scope=" {row, index} " slot="action">
                          <Button type="error" size="small" @click="removeStrategy(index)">Delete</Button>
                        </template>
                      </Table>
                      <Button type="primary" class="submit-button" @click="submitData">Submit</Button>
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
                    <div class="chart">
                      <h2>Line chart</h2>
                      <linechart/>
                    </div>

                </Card>
            </Content>
            <Footer class="layout-footer-center">2019 &copy; TalkingData</Footer>
        </Layout>
    </div>

    <!-- <router-view/> -->
  </div>
</template>

<script>
// import Schart from 'vue-schart';
import LineChart from '@/components/LineChart'

export default {
  data() {
    return {
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
      tableStrategyData: []
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
      this.tableProductData.push({assetClass: this.modelProduct, security: this.modelSecurity})
      console.log(this.tableProductData)
      this.modelProduct = ''
      this.modelSecurity = ''
    },

    removeProduct(index) {
      this.tableProductData.splice(index, 1)
    },

    addStrategy() {
      this.tableStrategyData.push({strategy: this.modelStrategy})
      console.log(this.tableStrategyData)
    },

    removeStrategy(index) {
      this.tableStrategyData.splice(index, 1)
    },

    getSecurityData() {
      // get securties data from asset class
      if (this.modelProduct == 'NASDAQ') {
        this.security = [
        {
          value: 'IBM',
          label: 'IBM'
        },
        {
          value: 'GBPUSD',
          label: 'GBPUSD'
        }]
      }
      else {
        this.security = []
      } 
    },

    submitData() {
      // submit all data to backend
      console.log('click submit button:' + '/config')
      this.axios({
        method: 'post',
        url: '/config',
        data: {
          startTime,
          endTime,
          modelFrequency,
          tableProductData,
          tableStrategyData
        }
      })
    }
  },
  components: {
    'linechart': LineChart
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
