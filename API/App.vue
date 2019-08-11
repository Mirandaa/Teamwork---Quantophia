<template>
  <div id="app">
    <img src="./assets/logo.png">
    <schart class="wrapper" :canvasId="canvasId" :type="type" :data="data" :options="options"></schart>
    <router-view/>
  </div>
</template>

<script>
export default {
    data() {
        return {
        time:'',
        }
    },
    methods:{
        handleClick(){
          this.$Message('It works!');
        }，
        getData(){
          this.$axios.get("the date file path")
          .then((response)=>{
            this.time = response.data.ChartName
          })
          .catch((error)=>{
            console.log(error)
          })
        }
     },
     mounted(){ /*生命周期函数*/
       this.getData();
     }
    }



</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.wrapper {
  width: 500px;
  height: 400px;
}
</style>
