import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Account from './Account.vue'
import Home from './views/Home.vue'
import store from '../../store'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "About" */ './views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: '/Account/',
  routes
})

export default router


new Vue({
  router,
  store,
  render: h => h(Account)
}).$mount('#app')
