<template>
	<div>
	<div v-for='returnData in chartData' class="single-result">
		<h2 class="titleName"> {{ getSecName(returnData) }}</h2>
		<Table :columns="resultDataColumns" :data="getCalcuData(returnData)" class="data-table">
			<template slot-scope="{ row }" slot="strategy">
				<strong>{{ row.strategy }}</strong>
			</template>
		</Table>
		<line-chart :data="{labels: getDate(returnData), datasets: getDataSets(returnData)}" :options="testOptions"/>
	</div>
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

	    testOptions: {
	      responsive: true,
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

		getDate(secNum) {
			this.chartData = this.getData()
			return secNum.date
		},

		getSecName(secNum) {
			return secNum.secName
		},

		getLabel(secNum, i) {
			return secNum.calcResult[i].stratName
		},

		getMarketData(secNum) {
			return secNum.marketData
		},

		getRegimeData(secNum, i) {
			return secNum.calcResult[i].regime
		},

		getTransColor() {
			return 'rgba(225,103,110,0)'
		},

		getBorderColor(i) {
			var colorList = ['rgba(225,103,110,1)', 'rgba(5,203,225,1)', 'rgba(65,105,225,1)', 'rgba(144,238,144,1)']
			return colorList[i]
		},

		getYield(secNum, i) {
			return secNum.calcResult[i].Yield
		},

		getBenchmark(secNum, i) {
			return secNum.calcResult[i].Benchmark
		},

		getSharpeRatio(secNum, i) {
			return secNum.calcResult[i].SharpeRatio
		},

		getAlpha(secNum, i) {
			return secNum.calcResult[i].Alpha
		},

		getBeta(secNum, i) {
			return secNum.calcResult[i].Beta
		},

		getMaxDrawdown(secNum, i) {
			return secNum.calcResult[i].MaxDrawdown
		},

		getCalcuData(sec) {
			var calcuData = []
			for (var i = 0; i < sec.calcResult.length; i++) {
				calcuData.push({
					strategy: this.getLabel(sec, i), 
					yield: this.getYield(sec, i), 
					benchmark: this.getBenchmark(sec, i), 
					sharpeRatio: this.getSharpeRatio(sec, i), 
					alpha: this.getAlpha(sec, i), 
					beta: this.getBeta(sec, i), 
					maxDrawdown: this.getMaxDrawdown(sec, i)
				})
			}
			return calcuData
		},

		getDataSets(sec) {
			var dataset = []
			dataset.push({label: 'Market', 
					fill: false,
					pointRadius: 0,
					backgroundColor: 'rgba(255,215,0,1)', 
					borderColor: 'rgba(255,215,0,1)', 
					pointBorderColor: this.getTransColor(), 
					data: this.getMarketData(sec)
			})
			for (var i = 0; i < sec.calcResult.length; i++) {
				dataset.push({
					label: this.getLabel(sec, i), 
					fill: false,
					pointRadius: 0,
					backgroundColor: this.getBorderColor(i), 
					borderColor: this.getBorderColor(i), 
					pointBorderColor: this.getTransColor(), 
					data: this.getRegimeData(sec, i)
				})
			}
			return dataset
		}
	}
}
</script>

<style>
.single-result {
	padding-bottom: 10px;
  margin-bottom: 20px;
  border-bottom: solid #e8eaec 1px;
}

.titleName {
	padding-bottom: 10px;
	text-align: center;
}

</style>