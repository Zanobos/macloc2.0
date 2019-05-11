<template>
  <div>
    <b-card v-for="user in users" :key="user.id" class="mb-1">
      <b-card-body>
        <b-row>
          <b-col>
            <p class="card-text" style="text-align: left">
                <ul>
                  <li>Name: {{ user.name }} </li>
                  <li>Nickname: {{ user.nickname }} </li>
                  <li>Email: {{ user.email }} </li>
                  <li>Height: {{ user.height}} </li>
                  <li>Weight: {{ user.weight}} </li>
                </ul>
              </p>
          </b-col>
          <b-col cols="3">
            <b-row class="mb-1">
              <b-button type="submit" variant="primary" @click="showEditModal(user)">Edit</b-button>
            </b-row>
            <b-row>
              <b-button variant="danger" @click="showDeleteModal(user)">Delete</b-button>
            </b-row>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>
    <b-modal ref="modalDeleteRef"
        centered
        hide-footer
        title="Delete Hold">
        <div>You are about to delete the user {{this.toDeleteUser.id}}.</div>
        <div>The procedure is irreversible. Do you want to proceed?</div>
        <b-btn class="mt-1" variant="danger" @click="deleteAndHideModal()">Delete</b-btn>
    </b-modal>
    <b-modal ref="modalEditRef"
      centered
      hide-footer
      title="Edit Hold">
      <form-user v-bind:initialUser="toEditUser" v-on:submit-user="onSubmitEditedUser"></form-user>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import FormUser from '@/components/forms/FormUser.vue'

export default {
  components: {
    FormUser
  },
  data () {
    return {
      toDeleteUser: {},
      toEditUser: {}
    }
  },
  computed: mapState({
    users: state => state.users.users
  }),
  methods: {
    ...mapActions({
      fetchUsers: 'users/fetchUsers',
      deleteUser: 'users/deleteUser',
      editUser: 'users/editUser'
    }),
    showEditModal (user) {
      this.toEditUser = user
      this.$refs.modalEditRef.show()
    },
    onSubmitEditedUser (user) {
      var payload = user
      var modalRef = this.$refs.modalEditRef
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.editUser(payload)
    },
    showDeleteModal (user) {
      this.toDeleteUser = user
      this.$refs.modalDeleteRef.show()
    },
    deleteAndHideModal (user) {
      var payload = {}
      var modalRef = this.$refs.modalDeleteRef
      payload.userId = this.toDeleteUser.id
      payload.onResponse = function (response) {
        modalRef.hide()
      }
      this.deleteUser(payload)
    }
  },
  created () {
    this.fetchUsers()
  }
}
</script>
