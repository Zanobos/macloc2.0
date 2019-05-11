<template>
  <div>
    <form-user v-bind:initialUser="{}" v-on:submit-user="onSubmitUser"></form-user>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import FormUser from '@/components/forms/FormUser.vue'

export default {
  components: {
    FormUser
  },
  methods: {
    onSubmitUser (hold) {
      this.createUser(hold)
    },
    ...mapActions({
      createUser: 'users/createUser'
    })
  }
}
</script>
