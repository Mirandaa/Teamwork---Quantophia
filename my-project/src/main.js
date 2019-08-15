// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import router from './router'
import axios from 'axios'
import moment from 'moment'
import '../static/style.css'

Vue.use(iView)
Vue.prototype.axios = axios
Vue.config.productionTip = false
axios.defaults.baseURL = 'http://127.0.0.1:8899/api'
axios.defaults.headers.post['Content-Type'] = 'application/json'

axios.interceptors.request.use(function (config) {
  // do something before request
  return config
}, function (error) {
  // do something when request be error
  return Promise.reject(error)
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App)
})
