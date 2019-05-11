import Vue from 'vue'
import { defaultErrorHandler } from '@/api'
import apiclimbs from '@/api/modules/apiclimbs'
import apiwalls from '@/api/modules/apiwalls'
import apiholds from '@/api/modules/apiholds'

const state = {
  isConnected: false,
  rtholds: {},
  ongoingClimbs: {}
}

const getters = {
  getForceByHoldId (state) {
    return (direction, holdId) => {
      if (state.rtholds[holdId] == null) {
        return null
      }
      return state.rtholds[holdId][direction]
    }
  },
  ongoingClimb (state) {
    return (wallId) => {
      return state.ongoingClimbs[wallId]
    }
  }
}

const actions = {
  socket_connect (context, payload) {
    context.commit('changeConnectionState', { isConnected: true })
  },
  socket_disconnect (context, payload) {
    context.commit('changeConnectionState', { isConnected: false })
  },
  socket_json (context, payload) {
    context.commit('storeRecord', { record: JSON.parse(payload) })
  },
  getOngoingClimbs (context) {
    apiclimbs.getClimbs(
      (response) => {
        context.commit('clearOngoingClimbs')
        response.data.items.forEach(climb => {
          context.commit('addOngoingClimb', { ongoingClimb: climb })
          context.dispatch('addOngoingWall', { wallId: climb.wall_id })
          context.dispatch('addOngoingHolds', { wallId: climb.wall_id })
        })
      },
      (error) => defaultErrorHandler(error),
      { not_status: 'end' }
    )
  },
  addOngoingWall (context, payload) {
    apiwalls.getWall(
      (response) => {
        context.commit('addOngoingWall', { ongoingWall: response.data })
      },
      (error) => defaultErrorHandler(error),
      payload.wallId
    )
  },
  addOngoingHolds (context, payload) {
    apiholds.getHolds(
      (response) => {
        context.commit('addOngoingHolds', { wallId: payload.wallId, ongoingHolds: response.data.items })
      },
      (error) => defaultErrorHandler(error),
      payload
    )
  }
}

const mutations = {
  changeConnectionState (state, { isConnected }) {
    state.isConnected = isConnected
  },
  storeRecord (state, { record }) {
    Vue.set(state.rtholds, record.hold_id, { x: record.x, y: record.y, z: record.z })
  },
  clearOngoingClimbs (state) {
    state.ongoingClimbs = {}
    state.rtholds = {}
  },
  addOngoingClimb (state, { ongoingClimb }) {
    Vue.set(state.ongoingClimbs, ongoingClimb.wall_id, ongoingClimb)
  },
  addOngoingWall (state, { ongoingWall }) {
    Vue.set(state.ongoingClimbs[ongoingWall.id], 'height', ongoingWall.height)
    Vue.set(state.ongoingClimbs[ongoingWall.id], 'width', ongoingWall.width)
    Vue.set(state.ongoingClimbs[ongoingWall.id], 'img', ongoingWall.img)
  },
  addOngoingHolds (state, { wallId, ongoingHolds }) {
    Vue.set(state.ongoingClimbs[wallId], 'holds', ongoingHolds)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
