import apiclimbs from '@/api/modules/apiclimbs'
import { defaultErrorHandler } from '@/api'

const state = {
  climbs: [],
  climbsMeta: {} // pagination not used any more
}

const getters = {}

const actions = {
  fetchClimbs ({ commit }, payload) {
    apiclimbs.getClimbs(
      (response) => {
        commit('storeClimbs', { climbs: response.data.items })
        commit('storeClimbsMeta', { meta: response.data._meta })
      },
      (error) => defaultErrorHandler(error),
      payload != null ? payload : {} // It's a query
    )
  },
  initClimbsMeta ({ commit }, payload) {
    commit('storeClimbsMeta', { meta: payload })
  },
  createClimb (context, payload) {
    apiclimbs.postClimbs(
      (response) => {
        context.dispatch('realtime/getOngoingClimbs', null, { root: true })
        if (typeof payload.onResponse === 'function') {
          payload.onResponse(response)
        }
      },
      (error) => defaultErrorHandler(error),
      payload.climb,
      { userId: payload.userId, wallId: payload.wallId }
    )
  },
  startClimb (context, payload) {
    var climb = {}
    climb.id = payload.climbId
    climb.status = 'start'
    apiclimbs.patchClimb(
      (response) => {
        context.dispatch('realtime/getOngoingClimbs', null, { root: true })
      },
      (error) => defaultErrorHandler(error),
      climb
    )
  },
  endClimb (context, payload) {
    var climb = {}
    climb.id = payload.climbId
    climb.status = 'end'
    apiclimbs.patchClimb(
      (response) => {
        context.dispatch('realtime/getOngoingClimbs', null, { root: true })
      },
      (error) => defaultErrorHandler(error),
      climb
    )
  },
  getClimb (context, payload) {
    apiclimbs.getClimb(
      (response) => {
        if (typeof payload.onResponse === 'function') {
          payload.onResponse(response)
        }
      },
      (error) => defaultErrorHandler(error),
      payload.climbId
    )
  },
  deleteClimb (context, payload) {
    apiclimbs.deleteClimb(
      (response) => {
        context.dispatch('realtime/getOngoingClimbs', null, { root: true })
        if (typeof payload.onResponse === 'function') {
          payload.onResponse(response)
        }
      },
      (error) => defaultErrorHandler(error),
      payload.climbId
    )
  }
}

const mutations = {
  storeClimbs (state, { climbs }) {
    state.climbs = climbs
  },
  storeClimbsMeta (state, { meta }) {
    state.climbsMeta = meta
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
