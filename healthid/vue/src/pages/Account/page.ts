import Vue from 'vue'
import Account from './Account.vue'
import router from './router'
import store from '../../store'

new Vue({
  router,
  store,
  render: h => h(Account)
}).$mount('#app')
