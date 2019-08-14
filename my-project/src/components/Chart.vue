<template>
	<div>
		<div v-for='returnData in chartData' class="single-result">
			<h2 class="titleName"> {{ getSecName(returnData) }}</h2>
			<line-chart :data="{labels: getDate(returnData), datasets: getDataSets(returnData)}" :options="testOptions"/>
			<Table border size="small" :columns="resultDataColumns" :data="getCalcuData(returnData)">
				<template slot-scope="{ row }" slot="strategy">
					<strong>{{ row.strategy }}</strong>
				</template>
			</Table>

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
        	title: 'Performance VS Market',
        	align: 'center',
        	children: [
		        {
		          title: 'Performance',
		          key: 'performance',
		          sortable: true,
		          width: 130,
		          render:(h, params) => {
		          	// 需要延迟处理，否则颜色无法赋值
		          	setTimeout(() => {
		          	}, 20)
		          	return h('span', {
		          		style: {
		          			color: (parseFloat(params.row.performance) > 0) ? "#f44336" : (parseFloat(params.row.performance) < 0 ? "#388e3c" : "#515a6e")
		          		}
		          	}, params.row.performance)
		          }
		        },
		        {
		          title: 'Market',
		          key: 'market',
		          sortable: true,
		          render:(h, params) => {
		          	// 需要延迟处理，否则颜色无法赋值
		          	setTimeout(() => {
		          	}, 20)
		          	return h('span', {
		          		style: {
		          			color: (parseFloat(params.row.market) > 0) ? "#f44336" : (parseFloat(params.row.market) < 0 ? "#388e3c" : "#515a6e")
		          		}
		          	}, params.row.market)
		          }
		        },
		        {
		          title: 'Diff',
		          key: 'diff',
		          sortable: true
		        }
	        ]
        },
        {
        	title: '???',
        	align: 'center',
        	children: [
	        	{
		          title: 'Annualized Return',
		          key: 'annReturn',
		          sortable: true,
		          width: 160,
		          render:(h, params) => {
		          	// 需要延迟处理，否则颜色无法赋值
		          	setTimeout(() => {
		          	}, 20)
		          	return h('span', {
		          		style: {
		          			color: (parseFloat(params.row.annReturn) > 0) ? "#f44336" : (parseFloat(params.row.annReturn) < 0 ? "#388e3c" : "#515a6e")
		          		}
		          	}, params.row.annReturn)
		          }
		        },
		        {
		          title: 'Max Drawdown',
		          key: 'maxDrawdown',
		          sortable: true,
		          width: 150,
		          render:(h, params) => {
		          	// 需要延迟处理，否则颜色无法赋值
		          	setTimeout(() => {
		          	}, 20)
		          	return h('span', {
		          		style: {
		          			color: (parseFloat(params.row.maxDrawdown) > 0) ? "#f44336" : (parseFloat(params.row.maxDrawdown) < 0 ? "#388e3c" : "#515a6e")
		          		}
		          	}, params.row.maxDrawdown)
		          }
		        }
        	]
        },
        {
        	title: 'Risk Index',
        	align: 'center',
        	children: [
		        {
		          title: 'Alpha',
		          key: 'alpha',
		          sortable: true
		        },
		        {
		          title: 'Beta',
		          key: 'beta',
		          sortable: true
		        },
		        {
		          title: 'Sharpe Ratio',
		          key: 'sharpeRatio',
		          sortable: true,
		          width: 130
		        }
        	]
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
			var colorList = ['rgba(225,103,110,1)', 'rgba(45,183,245,1)', 'rgba(65,105,225,1)', 'rgba(144,238,144,1)', 'rgba(255,182,193,1)', 'rgba(186,85,211,1)']
			return colorList[i]
		},

		getPerformance(secNum, i) {
			return secNum.calcResult[i].Performance
		},

		getMarket(secNum, i) {
			return secNum.calcResult[i].Market
		},

		getDiff(secNum, i) {
			return secNum.calcResult[i].Diff
		},

		getAnnReturn(secNum, i) {
			return secNum.calcResult[i].AnnualizedReturn
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
					performance: this.getPerformance(sec, i), 
					market: this.getMarket(sec, i), 
					diff: this.getDiff(sec, i),
					annReturn: this.getAnnReturn(sec, i),
					maxDrawdown: this.getMaxDrawdown(sec, i),
					alpha: this.getAlpha(sec, i), 
					beta: this.getBeta(sec, i),
					sharpeRatio: this.getSharpeRatio(sec, i)
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
	},

	created() {
		let transData = this.$route.query.allData
		this.chartData = tansData
	},

	watch: {
		'$route' (to, from) {
			if (to.query.allData != from.query.allData) {
				this.chartData = to.query.allData
			}
		}
	}
}
</script>

<style>
.single-result {
	padding-bottom: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  border-bottom: solid #e8eaec 1px;
}

.titleName {
	padding-bottom: 10px;
	text-align: center;
}

</style>