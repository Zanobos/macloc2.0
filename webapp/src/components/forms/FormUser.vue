<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="nameInputGroup"
                    label="Name:"
                    label-for="nameInput"
                    horizontal>
        <b-form-input id="nameInput"
                      type="text"
                      v-model="user.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-form-group id="nicknameInputGroup"
                    label="Nickname:"
                    label-for="nicknameInput"
                    horizontal>
        <b-form-input id="nicknameInput"
                      type="text"
                      v-model="user.nickname"
                      required
                      placeholder="Enter nickname">
        </b-form-input>
      </b-form-group>
      <b-form-group id="emailInputGroup"
                    label="Email address:"
                    label-for="emailInput"
                    description="We'll never share your email with anyone else."
                    horizontal>
        <b-form-input id="emailInput"
                      type="email"
                      v-model="user.email"
                      placeholder="Enter email">
        </b-form-input>
      </b-form-group>
      <b-form-group id="heightInputGroup"
                    label="Height (in cm):"
                    label-for="heightInput"
                    horizontal>
        <b-form-input id="heightInput"
                      required
                      v-model="user.height">
        </b-form-input>
      </b-form-group>
      <b-form-group id="weightInputGroup"
                    label="Weight (in cm):"
                    label-for="weightInput"
                    horizontal>
        <b-form-input id="weightInput"
                      required
                      v-model="user.weight">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  props: {
    initialUser: Object
  },
  data () {
    return {
      show: true
    }
  },
  computed: {
    user () {
      return Vue.util.extend({}, this.initialUser)
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('submit-user', this.user)
    },
    onReset (evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.user.name = this.initialUser.name
      this.user.nickname = this.initialUser.nickname
      this.user.email = this.initialUser.email
      this.user.height = this.initialUser.height
      this.user.weight = this.initialUser.weight
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  }
}
</script>
