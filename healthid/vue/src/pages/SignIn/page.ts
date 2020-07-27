import Vue from 'vue'
import Page from './SignIn.vue'
import store from '../../store'

Vue.config.productionTip = false

new Vue({
    render: h => h(Page),
  }).$mount('#app')