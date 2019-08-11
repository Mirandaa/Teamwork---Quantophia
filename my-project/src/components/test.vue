<template>
</template>

<script>
export default {
	data: {
		modelProduct: 'NASDAQ'
	},

  methods: {
      getSecurityData() {
      this.axios({
        method: 'get',
        url: 'http://192.168.43.141:8899/api/getSecurity',
        params: {
          asset_class: this.modelProduct
        }
      })
      .then(function (response) {
        console.log('response:' + response.data)
      }).catch(function(err) {
        console.log(err)
      })
    },
  },
  created () {
      this.getSecurityData()
  }
}

</script>
<style>
</style>



