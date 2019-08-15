<template>
	<div>    
		<div v-if="chartData.length == 1 | chartData[0].calcResult.length > 1">
      <div v-for='returnData in chartData' class="single-result">
				<h2 class="titleName"> {{ getSecName(returnData) }}</h2>
				<div> 				
					<line-chart :data="{labels: getDate(returnData), datasets: getDataSets(returnData)}" :options="testOptions"/>
				</div>

				<Table border size="small" :columns="resultDataColumns" :data="getCalcuData(returnData)">
					<template slot-scope="{ row }" slot="strategy">
						<strong>{{ row.strategy }}</strong>
					</template>
				</Table>
			</div>
    </div>

    <div v-else>
      <div class="single-result">
    		<h2 class="titleName" > Strategy - {{ chartData[0].calcResult[0].stratName }}</h2>
    		<div>
    			<line-chart :data="{labels: getDate(chartData[0]), datasets: getCalcuDataSets(chartData)}" :options="testOptions"/>
    		</div>
   			<Table border size="small" :columns="resultDataColumns" :data="getNCalcuData(chartData)">
					<template slot-scope="{ row }" slot="strategy">
						<strong>{{ row.strategy }}</strong>
					</template>
				</Table>
  		</div>
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
		          sortable: true,
		          width: 120
		        }
	        ]
        },
      	{
          title: 'Annualized Return',
          key: 'annReturn',
          sortable: true,
          width: 160,
          align: 'center',
          render:(h, params) => {
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
        	title: 'Risk Index',
        	align: 'center',
        	children: [
		        {
		          title: 'Alpha',
		          key: 'alpha',
		          sortable: true,
		          width: 100
		        },
		        {
		          title: 'Beta',
		          key: 'beta',
		          sortable: true,
		          width: 100
		        },
		        {
		          title: 'Sharpe Ratio',
		          key: 'sharpeRatio',
		          sortable: true,
		          width: 130
		        },
		        {
		          title: 'Max Drawdown',
		          key: 'maxDrawdown',
		          sortable: true,
		          width: 150,
		          align: 'center',
		          render:(h, params) => {
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
							labelString: 'Profit (%)'
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
			var colorList = ['rgba(46,199,201,1)', 'rgba(182,162,222,1)', 'rgba(90,177,239,1)', 'rgba(255,185,128,1)', 'rgba(216,122,128,1)', 'rgba(141,152,179,1)']
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

		// 1 prd - 1/n strategy
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
					borderWidth: 2,
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
					borderWidth: 2,
					pointBorderColor: this.getTransColor(),
					data: this.getRegimeData(sec, i)
				})
			}
			return dataset
		},

		// n prods - 1 strategy
		getNCalcuData(secList) {
			var calcuData = []
			for (var i = 0; i < secList.length; i++) {
				calcuData.push({
					strategy: this.getLabel(secList[i], 0) + ' - ' + this.getSecName(secList[i]), 
					performance: this.getPerformance(secList[i], 0), 
					market: this.getMarket(secList[i], 0), 
					diff: this.getDiff(secList[i], 0),
					annReturn: this.getAnnReturn(secList[i], 0),
					maxDrawdown: this.getMaxDrawdown(secList[i], 0),
					alpha: this.getAlpha(secList[i], 0), 
					beta: this.getBeta(secList[i], 0),
					sharpeRatio: this.getSharpeRatio(secList[i], 0)
				})
			}
			return calcuData
		},

		getCalcuDataSets(secList) {
			var dataset = []
			for (var i = 0; i < secList.length; i++) {
				dataset.push({
					label: this.getLabel(secList[i], 0)+"_"+secList[i].secName, 
      		fill: false,
      		pointRadius: 0,
      		backgroundColor: this.getBorderColor(i),
      		borderColor: this.getBorderColor(i),
      		borderWidth: 2,
      		pointBorderColor: this.getTransColor(), 
      		data: this.getRegimeData(secList[i], 0)
      	})
			}

			for (var i = 0; i < secList.length; i++) {
				dataset.push({
					label: "Market_" + secList[i].secName, 
					fill: false,
					pointRadius: 0,
					backgroundColor: this.getBorderColor(i),
					borderColor: this.getBorderColor(i),
					borderWidth: 2,
					borderDash: [5, 2],
					pointBorderColor: this.getTransColor(), 
					data: secList[i].marketData
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
				this.reload()
			}
		}
	}
}
</script>
