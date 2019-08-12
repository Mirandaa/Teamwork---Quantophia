// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue' // 就像你要引入jQuery一样，vue就是jquery-min.js，然后Vue就是$
import App from './App' // 同级目录下App.Vue文件（引入App这个组件）
import iView from 'iview'; // 引入iview UI组件
import 'iview/dist/styles/iview.css';
import router from './router' // 引入一段路由配置
import axios from 'axios'

Vue.use(iView)
Vue.prototype.axios = axios //Vue.prototype.名字(这个名字随便起，一般是叫$http或者$https，那么一看就明白，你这是在往后端发送请求)
Vue.config.productionTip = false
axios.defaults.baseURL = 'http://127.0.0.1:8899/api'
axios.defaults.headers.post['Content-Type'] = 'application/json'

axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
  return config
}, function (error) {
    // 对请求错误做些什么
  return Promise.reject(error)
})

/* eslint-disable no-new */
new Vue({
  el: '#app', /*最后效果将会替换页面中id为app的div元素*/
  router, /*使用路由*/
  components: { App }, /*告知当前页面想使用App这个组件*/
  template: '<App/>', /*告知页面这个组件用这样的标签来包裹着,并且使用它*/
  render: h => h(App)
})
