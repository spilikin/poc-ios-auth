import Vue from 'vue'
import Vuex, { StoreOptions } from 'vuex';

Vue.use(Vuex)

export interface SecurityContext {
  token: string;
  jwt: object;
  acct: string;
}

export interface RootState {
  securityContext?: SecurityContext;
}

const store: StoreOptions<RootState> = {
  state: {
  },
  modules: {
  }
};

export default new Vuex.Store<RootState>(store);
