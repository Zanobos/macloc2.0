// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueSocketIO from 'vue-socket.io'
import io from 'socket.io-client'
import App from './App'
import router from './router'
import store from './store'
import { SOCKET_IO_URL, SOCKET_IO_PATH } from '@/api'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(BootstrapVue)

Vue.use(new VueSocketIO({
  debug: true,
  connection: io(SOCKET_IO_URL, {path: SOCKET_IO_PATH, transports: ['websocket']}),
  vuex: {
    store,
    actionPrefix: 'socket_'
  }
}))

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
