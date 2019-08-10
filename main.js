// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue' // 就像你要引入jQuery一样，vue就是jquery-min.js，然后Vue就是$
import App from './App' // 同级目录下App.Vue文件（引入App这个组件）
import router from './router' // 引入一段路由配置
import Axios from 'axios';


//API 接口

import {getRequest, postRequest} from './libs/api'; //
Vue.prototype.$axios = Axios
Axios.defaults.baseURL = '/api'
Axios.defaults.headers.post['Content-Type'] = 'application/json'

Vue.prototype.getRequest = getRequest;//注入到vue对象
Vue.prototype.postRequest = postRequest;//注入到vue对象

Vue.config.productionTip = false
Vue.use(AtUI)

/* eslint-disable no-new */
new Vue({
  el: '#app', /*最后效果将会替换页面中id为app的div元素*/
  router, /*使用路由*/
  render: h=> h(App) /???/
  components: { App }, /*告知当前页面想使用App这个组件*/
  template: '<App/>' /*告知页面这个组件用这样的标签来包裹着,并且使用它*/
})



