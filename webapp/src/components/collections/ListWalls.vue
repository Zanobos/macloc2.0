<template>
  <div>
    <b-card v-for="wall in walls" :key="wall.id" class="mb-1">
      <b-card-body>
        <b-row>
          <b-col>
            <p class="card-text" style="text-align: left">
              <ul>
                <li>Wall id: {{ wall.id }} </li>
                <li>Grade: {{ wall.grade }} </li>
                <li>Height: {{ wall.height }} </li>
                <li>Width: {{ wall.width }} </li>
                <li>Background: <div class="example-bg" :style="{ 'background-image': 'url(\'' + getImg(wall.img)+ '\')' }"></div></li>
              </ul>
            </p>
          </b-col>
          <b-col cols="3">
            <b-row class="mb-1">
              <b-button type="submit" variant="primary" @click="showEditModal(wall)">Edit</b-button>
            </b-row>
            <b-row>
              <b-button variant="danger" @click="showDeleteModal(wall)">Delete</b-button>
            </b-row>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>
    <b-modal ref="modalDeleteRef"
        centered
        hide-footer
        title="Delete Wall">
        <div>You are about to delete the wall {{this.toDeleteWall.id}}.</div>
        <div>The procedure is irreversible. Do you want to proceed?</div>
        <b-btn class="mt-1" variant="danger" @click="deleteAndHideModal()">Delete</b-btn>
    </b-modal>
    <b-modal ref="modalEditRef"
      centered
      hide-footer
      title="Edit Wall">
      <form-wall v-bind:initialWall="toEditWall" v-on:submit-wall="onSubmitEditedWall"></form-wall>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import { getWallImg } from '@/api'
import FormWall from '@/components/forms/FormWall.vue'

export default {
  components: {
    FormWall
  },
  data () {
    return {
      toDeleteWall: {},
      toEditWall: {}
    }
  },
  computed: {
    ...mapState({
      walls: state => state.walls.walls
    })
  },
  created () {
    this.fetchWalls()
  },
  methods: {
    ...mapActions({
      fetchWalls: 'walls/fetchWalls',
      deleteWall: 'walls/deleteWall',
      editWall: 'walls/editWall'
    }),
    getImg: getWallImg,
    showEditModal (wall) {
      this.toEditWall = wall
      this.$refs.modalEditRef.show()
    },
    onSubmitEditedWall (wall) {
      var payload = wall
      var modalRef = this.$refs.modalEditRef
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.editWall(payload)
    },
    showDeleteModal (wall) {
      this.toDeleteWall = wall
      this.$refs.modalDeleteRef.show()
    },
    deleteAndHideModal (wall) {
      var payload = {}
      var modalRef = this.$refs.modalDeleteRef
      payload.wallId = this.toDeleteWall.id
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.deleteWall(payload)
    }
  }
}
</script>

<style scoped>
.example-bg {
  display: inline-block;
  height: 20px;
  width: 100px;
}
</style>
