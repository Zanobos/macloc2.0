<template>
  <div>
    <b-form @submit="onSubmit" v-if="show">
      <b-form-group id="userInputGroup"
                    label="User:"
                    label-for="userInput">
        <b-form-select id="userInput"
          :options="users"
          v-model="selectedUser">
        <template slot="first">
          <option :value="null" disabled>-- Select a user --</option>
        </template>
        </b-form-select>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  props: {
    wallId: Number,
    users: Array
  },
  data () {
    return {
      show: true,
      selectedUser: null
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      var form = {}
      form.wallId = this.wallId
      form.userId = this.selectedUser.id
      this.$emit('submit-climb', form)
    }
  }
}
</script>
