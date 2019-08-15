import { Line } from 'vue-chartjs'

export default {
  name: 'linechart',
  extends: Line,
  props: ['data', 'options'],
  mounted () {
    this.renderChart(this.data, this.options)
  }
}
