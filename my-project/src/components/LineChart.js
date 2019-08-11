import { Line } from 'vue-chartjs'

export default {
  name: 'linechart',
  extends: Line, // 要引入的图形 (line是折线图)
  props: ['data', 'options'], //可以在以组件传参的形式定义data,和options配置
  //创建图形必须要在mounted函数里
  mounted () {
    this.renderChart({
      // labels 表示x轴的配置
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      xlabel: 'Date',
      // datasets 是个数组 表示线性走势及对走势线的配置
      datasets: [
        {
          label: 'MACD',
          backgroundColor: 'rgba(225,10,10,0)',
          borderColor: 'rgba(225,103,110,1)',
          pointBorderColor: 'rgba(225,103,110,0)',
          data: [40, 39, 10, 40, 39, 80, 40]
        },
        {
          label: 'KDJ',
          backgroundColor: 'rgba(5,203,225,0)',
          borderColor: 'rgba(5,203,225,1)',
          pointBorderColor: 'rgba(5,203,225,0)',
          data: [60, 55, 32, 10, 2, 12, 53]
        }
      ]
    }, 
    {
      responsive: true, 
      maintainAspectRatio: false
    })
    // 长宽，100%.如果要单设长和宽的话，要将responsive 设为false    maintainAspectRatio 保持长宽比  
  }
}
