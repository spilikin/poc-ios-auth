<template>
  <div class="authenticate">
      <canvas id="code"></canvas>
      <h1 class="h3 mb-3 font-weight-normal">Scan QR-Code using AuthApp</h1>
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
      QRCode.toCanvas(canvas, 'https://appauth.acme.spilikin.dev/SignInRemote?foo=bar', function (error: Error) {
        if (error) console.error(error)
      })
    });

  }

}
</script>

<style scoped>

</style>
