import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
    user: null,
    token: null,
  },

  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {},
  getters: {
    isLoggedIn(state) {
        return !!state.token
    },
    getUser() {
        return this.state.user
    },
    getToken() {
        return this.state.token
    },
  }
});

//source: https://www.loginradius.com/blog/engineering/implementing-authentication-on-vuejs-using-jwt/