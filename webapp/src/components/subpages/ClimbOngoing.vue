<template>
  <b-container>
    <b-row>
      <b-col cols="3">
        <b-button :disabled="prepareButtonDisabled()" class="w-100 mb-1" variant="primary" @click="showPrepareModal">Prepare</b-button>
        <b-button :disabled="deleteButtonDisabled()" class="w-100 mb-1" variant="danger" @click="showDeleteModal">Delete</b-button>
        <b-button :disabled="startButtonDisabled()" class="w-100 mb-1" variant="success" @click="onStart">Start</b-button>
        <b-button :disabled="endButtonDisabled()" class="w-100" variant="danger" @click="onEnd">End</b-button>
        <p>Connected?{{connected}}</p>
        <b-card
                v-for="hold in holds"
                :key="hold.id"
                class="mb-1">
          <b-card-body>
            <p class="card-text" style="text-align: left">
              <ul>
                <li>Id: {{ hold.id }} </li>
                <li>Type: {{ hold.hold_type }} </li>
                <li>Force 1: {{getForceByHoldId('x', hold.id)}}</li>
                <li>Force 2: {{getForceByHoldId('y', hold.id)}}</li>
                <li>Force 3: {{getForceByHoldId('z', hold.id)}}</li>
              </ul>
            </p>
          </b-card-body>
        </b-card>
      </b-col>
      <b-col>
        <real-time-holds-graph v-if="climb" :wallId="this.wallId"></real-time-holds-graph>
      </b-col>
    </b-row>
    <b-modal ref="modalSubmitRef"
      centered
      hide-footer
      title="Prepare Climb">
      <form-climb :users="users" :wallId="this.wallId" v-on:submit-climb="onSubmitNewClimb"></form-climb>
    </b-modal>
    <b-modal ref="modalDeleteRef"
      centered
      hide-footer
      title="Delete Climb">
      <div>You are about to delete the climb {{climbId}}.</div>
      <div>The procedure is irreversible. Do you want to proceed?</div>
      <b-btn class="mt-1" variant="danger" @click="deleteAndHideModal()">Delete</b-btn>
    </b-modal>
  </b-container>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import RealTimeHoldsGraph from '@/components/graphs/RealTimeHoldsGraph.vue'
import FormClimb from '@/components/forms/FormClimb.vue'

export default {
  props: {
    wallId: Number
  },
  components: {
    RealTimeHoldsGraph,
    FormClimb
  },
  computed: {
    ...mapState({
      connected: state => state.realtime.isConnected
    }),
    ...mapGetters({
      getForceByHoldId: 'realtime/getForceByHoldId',
      ongoingClimb: 'realtime/ongoingClimb',
      users: 'users/getUsersLabelledByName'
    }),
    climb () {
      return this.ongoingClimb(this.wallId) !== undefined ? this.ongoingClimb(this.wallId) : undefined
    },
    holds () {
      return this.climb !== undefined ? this.climb.holds : []
    },
    climbId () {
      return this.climb !== undefined ? this.climb.id : ''
    },
    climbStatus () {
      return this.climb !== undefined ? this.climb.status : 'no_climb'
    }
  },
  methods: {
    ...mapActions({
      createClimb: 'climbs/createClimb',
      startClimb: 'climbs/startClimb',
      endClimb: 'climbs/endClimb',
      deleteClimb: 'climbs/deleteClimb'
    }),
    prepareButtonDisabled () {
      return this.climbStatus !== 'no_climb'
    },
    deleteButtonDisabled () {
      return this.climbStatus !== 'ready'
    },
    startButtonDisabled () {
      return this.climbStatus !== 'ready'
    },
    endButtonDisabled () {
      return this.climbStatus !== 'start'
    },
    onSubmitNewClimb (climb) {
      var payload = climb
      var modalSubmitRef = this.$refs.modalSubmitRef
      payload.onResponse = function (response) {
        modalSubmitRef.hide()
      }
      this.createClimb(payload)
    },
    onStart (evt) {
      evt.preventDefault()
      var payload = {}
      payload.climbId = this.climbId
      this.startClimb(payload)
    },
    onEnd (evt) {
      evt.preventDefault()
      var payload = {}
      payload.climbId = this.climbId
      this.endClimb(payload)
    },
    deleteAndHideModal (wall) {
      var payload = {}
      var modalRef = this.$refs.modalDeleteRef
      payload.climbId = this.climbId
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.deleteClimb(payload)
    },
    showPrepareModal (evt) {
      this.$refs.modalSubmitRef.show()
    },
    showDeleteModal (evt) {
      this.$refs.modalDeleteRef.show()
    }
  }
}
</script>
