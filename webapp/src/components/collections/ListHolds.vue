<template>
  <div>
    <b-card v-for="hold in holds" :key="hold.id" class="mb-1">
      <b-card-body>
        <b-row>
          <b-col>
            <p class="card-text" style="text-align: left">
              <ul>
                <li>Hold id: {{ hold.id }} </li>
                <li>Can id: {{ hold.can_id }} </li>
                <li>Distance from left edge: {{ hold.dist_from_sx}} </li>
                <li>Distance from bottom: {{ hold.dist_from_bot}} </li>
                <li>Hold type: {{ hold.hold_type}} </li>
                <li>On wall: {{ hold.wall_id}} </li>
              </ul>
            </p>
          </b-col>
          <b-col cols="3">
            <b-row class="mb-1">
              <b-button type="submit" variant="primary" @click="showEditModal(hold)">Edit</b-button>
            </b-row>
            <b-row>
              <b-button variant="danger" @click="showDeleteModal(hold)">Delete</b-button>
            </b-row>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>
    <b-modal ref="modalDeleteRef"
        centered
        hide-footer
        title="Delete Hold">
        <div>You are about to delete the hold {{this.toDeleteHold.id}}.</div>
        <div>The procedure is irreversible. Do you want to proceed?</div>
        <b-btn class="mt-1" variant="danger" @click="deleteAndHideModal()">Delete</b-btn>
    </b-modal>
    <b-modal ref="modalEditRef"
      centered
      hide-footer
      title="Edit Hold">
      <form-hold v-bind:initialHold="toEditHold" v-bind:wallIds="wallIds" v-on:submit-hold="onSubmitEditedHold"></form-hold>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import FormHold from '@/components/forms/FormHold.vue'

export default {
  components: {
    FormHold
  },
  data () {
    return {
      toDeleteHold: {},
      toEditHold: {}
    }
  },
  computed: {
    ...mapState({
      holds: state => state.holds.holds
    }),
    ...mapGetters({
      wallIds: 'walls/wallIds'
    })
  },
  created () {
    this.fetchHolds()
  },
  methods: {
    ...mapActions({
      fetchHolds: 'holds/fetchHolds',
      deleteHold: 'holds/deleteHold',
      editHold: 'holds/editHold'
    }),
    showEditModal (hold) {
      this.toEditHold = hold
      this.$refs.modalEditRef.show()
    },
    onSubmitEditedHold (hold) {
      var payload = hold
      var modalRef = this.$refs.modalEditRef
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.editHold(payload)
    },
    showDeleteModal (hold) {
      this.toDeleteHold = hold
      this.$refs.modalDeleteRef.show()
    },
    deleteAndHideModal (hold) {
      var payload = {}
      var modalRef = this.$refs.modalDeleteRef
      payload.holdId = this.toDeleteHold.id
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.deleteHold(payload)
    }
  }
}
</script>
