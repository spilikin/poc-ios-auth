<template>
  <div class="authenticate">
      <canvas id="code"></canvas>
      <h1 class="h3 mb-3 font-weight-normal">Scan QR-Code using your Smartphone</h1>
      <a href="https://apps.apple.com/de/app/testflight/id899247664?mt=8" style="display:inline-block;overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2014-09-09&kind=iossoftware&bubble=ios_apps) no-repeat;width:135px;height:40px;"></a>
      <div>
        <a id="cancel" href="/SignIn/">Cancel</a>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import QRCode from 'qrcode'

@Component
export default class Identity extends Vue {
  mounted() {
      this.$nextTick(function () {
      const canvas = document.getElementById('code')
      let url = 'https://appauth.acme.spilikin.dev/api/auth/remote'
      url += "?acct="+this.$route.query['acct']
      url += "&nonce="+this.$route.query['nonce']
      url += "&redirect_uri="+this.$route.query['redirect_uri']
      console.log(url)
      QRCode.toCanvas(canvas, url , function (error: Error) {
        if (error) console.error(error)
      })
    });

  }

}
</script>

<style scoped>

</style>
