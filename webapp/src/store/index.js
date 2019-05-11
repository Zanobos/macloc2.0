import Vue from 'vue'
import Vuex from 'vuex'
import walls from './modules/walls'
import climbs from './modules/climbs'
import users from './modules/users'
import holds from './modules/holds'
import realtime from './modules/realtime'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    walls,
    climbs,
    users,
    holds,
    realtime
  }
})
