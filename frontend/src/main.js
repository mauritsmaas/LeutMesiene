// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from '../plugins/vuetify'
import VueSimpleAlert from "vue-simple-alert";



Vue.config.productionTip = false
Vue.use(VueSimpleAlert)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  vuetify,
  VueSimpleAlert,
  components: { App },
  template: '<App/>'
})
