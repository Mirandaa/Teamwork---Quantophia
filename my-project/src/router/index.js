import Vue from 'vue'
import Router from 'vue-router'
import test from '@/components/test'
import Chart from '@/components/Chart'

Vue.use(Router)

export default new Router({
  routes: [
    {
    	path: '/test',
    	name: 'test',
    	component: test
    },
    {
      path: '/Chart',
      name: 'Chart',
      component: Chart
    }
  ]
})
