<template>
	<div>
		<Table :columns="resultDataColumns" :data=getCalcuData() class="data-table">
			<template slot-scope="{ row }" slot="strategy">
				<strong>{{ row.strategy }}</strong>
			</template>
		</Table>
		<!-- <p>{{ chartData[0].calcResult[0].Benchmark }}</p> -->
		<line-chart :data="testData" :options="testOptions"/>

	</div>
</template>

<script>
import LineChart from './LineChart'

export default {
	inject: ['reload'],
	components: {
		LineChart
	},

	data() {
		return {
			chartData: this.getData(),

			resultDataColumns: [
        {
          title: 'Strategy',
          key: 'strategy'
        },
        {
          title: 'Yield',
          key: 'yield'
        },
        {
          title: 'Benchmark',
          key: 'benchmark'
        },
        {
          title: 'Sharpe Ratio',
          key: 'sharpeRatio'
        },
        {
          title: 'Alpha',
          key: 'alpha'
        },
        {
          title: 'Beta',
          key: 'beta'
        },
        {
          title: 'Max Drawdown',
          key: 'maxDrawdown'
        }
      ],

			testData: {
	      // labels 表示x轴的配置
	      labels: this.getDate(),
	      // datasets 是个数组 表示线性走势及对走势线的配置
	      datasets: this.getDataSets()
	    },

	    testOptions: {
	      responsive: true,
	      title: {
					display: true,
					text: this.getSecName()
				},
	      maintainAspectRatio: false,
	      tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'index',
					intersect: false
				},
				scales: {
					xAxes: [{
						type: 'time',
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Profit'
						}
					}]
				}
	    }
		}
	},

	methods: {
		refreshTable() {
      this.reload()
    },

    // 从submit提交之后的response获取返回的数据
		getData() {
			return this.$route.query.allData
		},

		getDate() {
			this.chartData = this.getData()
			return this.chartData[0].date
		},

		getSecName() {
			return this.chartData[0].secName
		},

		getLabel(i) {
			return this.chartData[0].calcResult[i].stratName
		},

		getMarketData() {
			return this.chartData[0].marketData
		},

		getRegimeData(i) {
			return this.chartData[0].calcResult[i].regime
		},

		getTransColor() {
			return 'rgba(225,103,110,0)'
		},

		getBorderColor(i) {
			var colorList = ['rgba(225,103,110,1)', 'rgba(5,203,225,1)', 'rgba(65,105,225,1)']
			return colorList[i]
		},

		getYield(i) {
			return this.chartData[0].calcResult[i].Yield
		},

		getBenchmark(i) {
			return this.chartData[0].calcResult[i].Benchmark
		},

		getSharpeRatio(i) {
			return this.chartData[0].calcResult[i].SharpeRatio
		},

		getAlpha(i) {
			return this.chartData[0].calcResult[i].Alpha
		},

		getBeta(i) {
			return this.chartData[0].calcResult[i].Beta
		},

		getMaxDrawdown(i) {
			return this.chartData[0].calcResult[i].MaxDrawdown
		},

		getCalcuData() {
			var calcuData = []
			for (var i = 0; i < this.chartData[0].calcResult.length; i++) {
				calcuData.push({
					strategy: this.getLabel(i), 
					yield: this.getYield(i), 
					benchmark: this.getBenchmark(i), 
					sharpeRatio: this.getSharpeRatio(i), 
					alpha: this.getAlpha(i), 
					beta: this.getBeta(i), 
					maxDrawdown: this.getMaxDrawdown(i)
				})
			}
			return calcuData
		},

		getDataSets() {
			var dataset = []
			dataset.push({label: 'Market', 
					fill: false,
					pointRadius: 0,
					backgroundColor: 'rgba(255,215,0,1)', 
					borderColor: 'rgba(255,215,0,1)', 
					pointBorderColor: this.getTransColor(), 
					data: this.getMarketData()
			})
			for (var i = 0; i < this.chartData[0].calcResult.length; i++) {
				dataset.push({
					label: this.getLabel(i), 
					fill: false,
					pointRadius: 0,
					backgroundColor: this.getBorderColor(i), 
					borderColor: this.getBorderColor(i), 
					pointBorderColor: this.getTransColor(), 
					data: this.getRegimeData(i)
				})
			}
			return dataset
		}
	}
}
</script>