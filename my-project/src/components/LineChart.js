import { Line } from 'vue-chartjs'

export default {
  name: 'linechart',
  extends: Line, // 要引入的图形 (line是折线图)
  props: ['data', 'options'], //可以在以组件传参的形式定义data,和options配置
  //创建图形必须要在mounted函数里
  mounted () {
    this.renderChart(this.data, this.options)
  }
}
