<template>
  <div class="home">
    <h1>Welcome to your HealthID</h1>
    <p>
    {{this.$store.state.securityContext.acct}}
    </p>
    <vue-json-pretty
      :path="'res'"
      :data="jwt">
    </vue-json-pretty>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import VueJsonPretty from 'vue-json-pretty'

@Component({
  components: { VueJsonPretty }
})
export default class Home extends Vue {
  acct: string
  jwt: object

  created() {
    this.acct = this.$store.state.securityContext.acct
    this.jwt = this.$store.state.securityContext.jwt
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