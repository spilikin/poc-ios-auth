import Vue from 'vue'
import Account from './Account.vue'
import router from './router'
import store, {SecurityContext} from './store'
import axios from 'axios';

function startVue() {
  new Vue({
    router,
    store,

    render: h => h(Account)
  }).$mount('#app')  
}

const vue = new Vue({
  router,
  store,
  render: h => h(Account)
})

const url = new URL(window.location.href);
const arr = url.href.split("/");
const redirectUri = arr[0]+'//'+arr[2]+'/Account'


new Promise<SecurityContext>((resolve, reject) => {
  new Promise<string>((resolveToken, rejectToken) => {
    // TODO: OWASP says HttpOnly is better than local storage for tokens
    const token = localStorage.getItem('access_token')
    if (typeof token === 'string') {
      resolveToken(token)
      return
    }
    const code = url.searchParams.get('code')

    // we received code, try to fetch the token
    if (typeof code === 'string') {
      const data = new FormData()
  
      data.append("grant_type", "authorization_code")
      data.append("client_id", "public_client")
      data.append("redirect_uri", ""+url.searchParams.get('redirect_uri'))
      data.append("code", code)
      data.append("code_verifier", "non implemented")
    
      axios.post('/api/auth/token', data)
      .then(response => {
        if (typeof response.data['access_token'] !== 'string') {
          throw Error("No token returned by the API")
        }
        resolveToken(response.data['access_token'])
        router.push("/")
      })
      .catch(error => {
        alert(error)
        window.location.href="/SignIn/?redirect_uri="+encodeURI(redirectUri)
      });
    
    } else {
      reject(new Error("No token available"))
    }
  })
  .then(token => {
    console.log(token)
    localStorage.setItem('access_token', token)
    const jwt =  JSON.parse(atob(token.split('.')[1]))
    
    resolve({
      token: token,
      jwt: jwt,
      acct: jwt['sub']
    })
    
  })
  .catch(error => reject(error))
}).then(securityContext => {
  store.state.securityContext = securityContext
  vue.$mount('#app')
}).catch(error => {
  console.error(error)
  window.location.href="/SignIn/?redirect_uri="+encodeURI(redirectUri)
})

/*
if (code != null) {
  const data = new FormData()
  
  data.append("grant_type", "authorization_code")
  data.append("client_id", "public_client")
  data.append("redirect_uri", ""+url.searchParams.get('redirect_uri'))
  data.append("code", code)
  //"code_verifier": "none",

  axios.post('/api/auth/token', data)
  .then(response => {
    if (typeof response.data['access_token'] !== 'string') {
      throw Error("No token returned by the API")
    }
    token = response.data['access_token']
    const jwt =  JSON.parse(atob(token.split('.')[1]))
    
    //const securityContext = new SecurityContext(token, jwt, jwt['sub'])
    store.state.securityContext = {
      token: token,
      jwt: jwt,
      acct: jwt['sub']
    }
    vue.$mount('#app')
  })
  .catch(error => {
    alert(error)
    window.location.href="/SignIn/?redirect_uri="+encodeURI(redirectUri)
  });
} else if (token == null) {
    window.location.href="/SignIn/?redirect_uri="+encodeURI(redirectUri)
} else {
  vue.$mount('#app')
}
*/