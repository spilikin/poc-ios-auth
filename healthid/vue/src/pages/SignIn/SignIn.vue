<template>
  <div id="signin">
    <div v-if="showCode">
      <canvas id="code"></canvas>
    </div>
    <img v-else class="logo" alt="HealthID" src="@/assets/logo.png">
    <div class="form-signin">
      <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
      <b-alert :show="error != ''" variant="danger" dismissible>
      {{ error }}
      </b-alert>
      <div v-if="state == 'account'">
        <label for="inputEmail" class="sr-only">Email address</label>
        <input v-model="account" type="email" id="account" class="form-control" placeholder="Enter your HealthID" required autofocus>
        <div class="checkbox mb-3">
          <label>
            <input @change="onRemember" v-model="remember" type="checkbox"> Remember me
          </label>
        </div>
        <button @click="onCheckAccount" class="btn btn-lg btn-primary btn-block">Continue</button>
      </div>
      <div v-if="state == 'authenticate'">
        <b-button @click="onAuthenticateViaApp" block variant="outline-primary"><b-icon icon="phone"></b-icon> Authenticate via App </b-button>
        <b-button @click="onShowCode" block variant="secondary"><b-icon icon="upc-scan"></b-icon> Scan SignIn Code</b-button>
        <a id="cancel" href="/SignIn/">Cancel</a>
      </div>
      <p class="mt-5 mb-3 text-muted">No password. No PIN. No cry.<br>
      <small>API Version {{ apiInfo }}</small>
      </p>
    </div>
  </div>  
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import QRCode from 'qrcode'
import axios from 'axios';

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

@Component
export default class SignIn extends Vue {
  account = ""
  remember = false
  state = "account"
  showCode = false
  apiInfo = "unknown"
  error = ""

  mounted() {
    this.account = localStorage.getItem("account") || ""
    this.remember = localStorage.getItem("account") != null
    axios.get("/api/info")
      .then(response => (this.apiInfo = response.data.version))
      .catch(reason => {
        console.debug(reason)
        this.error = reason
      })

  }

  onCheckAccount(

  ): void {
    console.log('Signin: '+this.account)
    if (this.remember) {
      localStorage.setItem("account", this.account)
    }
    this.state = "authenticate"
  }

  onRemember(): void {
    if (this.remember) {
      localStorage.setItem("account", this.account)
    } else {
      localStorage.removeItem("account")
    }
  }

  onAuthenticateViaApp(): void {
    window.location.href="https://appauth.acme.spilikin.dev/SignIn?foo=bar"
  }

  onShowCode(): void {
    this.showCode = true
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

html,
body {
  height: 100%;
}

#signin {
  padding: 40px;
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.logo {
  width:100%;
  max-width: 170px;
  border-radius: 15px;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  margin-bottom: 10px;
}

#cancel {
  display: block;
  padding: 10px;
  text-decoration: underline;
}
</style>
