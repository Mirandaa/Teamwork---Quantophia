<template>
  <div id="hello">
    <h1>site: {{ site }}</h1>
    <h1>team: {{ team }}</h1>
    <h1>score: {{ score }}</h1>
    <h1>details: {{ details() }}</h1>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      site: "Back Testing",
      team: "team16",
      score: 100
    }
  },
  methods: {
    details: function() {
      return  this.site + " - From Training Project";
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
