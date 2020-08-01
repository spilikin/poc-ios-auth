import Vue from 'vue'
import Page from './SignIn.vue'

Vue.config.productionTip = false

new Vue({
    render: h => h(Page),
  }).$mount('#app')