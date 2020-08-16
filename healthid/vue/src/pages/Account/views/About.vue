<template>
  <div class="about">
    <h1>{{this.$store.state.securityContext.acct}}</h1>
    <vue-json-pretty
      :path="'res'"
      :data="account">
    </vue-json-pretty>
  </div>
</template>


<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import VueJsonPretty from 'vue-json-pretty'
import axios from 'axios'

@Component({
  components: { VueJsonPretty }
})
export default class Home extends Vue {
  accountInfo: object = {}

  get account(): object {
    return this.accountInfo
  }

  created() {
    axios.get(`/api/acct/${this.$store.state.securityContext.acct}`, 
    this.$store.state.securityContext.axiosConfig)
    .then(response => {
      console.debug(response)
      this.accountInfo = response.data
    })
    .catch(error => {
      console.error(error)
    });
  }

}
</script>

<style scoped>
.vjs-tree, .is-root {
  text-align: left;
  margin: auto;
    width: 50%;
}
</style>