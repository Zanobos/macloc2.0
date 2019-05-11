import apiholds from '@/api/modules/apiholds'
import { defaultErrorHandler } from '@/api'

const state = {
  holds: [],
  holdsMeta: {} // not used anymore
}

const getters = {
  holdsMap (state) {
    return state.holds.reduce(function (map, hold) {
      map[hold.id] = hold
      return map
    }, {})
  }
}

const actions = {
  fetchHolds ({ commit }, payload) {
    apiholds.getHolds(
      (response) => {
        commit('storeHolds', { holds: response.data.items })
        commit('storeHoldsMeta', { meta: response.data._meta })
      },
      (error) => defaultErrorHandler(error),
      payload != null ? payload : {} // It's a query
    )
  },
  initHoldsMeta ({ commit }, payload) {
    commit('storeHoldsMeta', { meta: payload })
  },
  getOngoingHolds (context, payload) {
    apiholds.getHolds(
      (response) => {
        context.commit('realtime/setOngoingHolds', { ongoingHolds: response.data.items }, { root: true })
      },
      (error) => defaultErrorHandler(error),
      payload
    )
  },
  createHold (context, payload) {
    apiholds.postHolds(
      (response) => context.dispatch('fetchHolds'),
      (error) => defaultErrorHandler(error),
      payload
    )
  },
  deleteHold (context, payload) {
    apiholds.deleteHold(
      (response) => {
        context.dispatch('fetchHolds')
        if (typeof payload.onResponse === 'function') {
          payload.onResponse(response)
        }
      },
      (error) => defaultErrorHandler(error),
      payload.holdId
    )
  },
  editHold (context, payload) {
    apiholds.putHold(
      (response) => {
        context.dispatch('fetchHolds')
        if (typeof payload.onResponse === 'function') {
          payload.onResponse(response)
        }
      },
      (error) => defaultErrorHandler(error),
      payload
    )
  }
}

const mutations = {
  storeHolds (state, { holds }) {
    state.holds = holds
  },
  storeHoldsMeta (state, { meta }) {
    state.holdsMeta = meta
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
