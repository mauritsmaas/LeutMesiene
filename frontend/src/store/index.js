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
      state.user = {"user" : user};
    },
    setToken(state, token) {
      state.token = token;
    }
  },
  actions: {},
  getters: {
    user: state => state.user,
    token: state => state.token,
    is_valid: state => state.is_valid
  },
  computed: {
    isLoggedIn(state) {
      return !!state.token
    },
    getUser() {
      return this.$store.getters.user
    },
    getToken() {
      return this.$store.getters.token
    }
  }
});

//source: https://www.loginradius.com/blog/engineering/implementing-authentication-on-vuejs-using-jwt/