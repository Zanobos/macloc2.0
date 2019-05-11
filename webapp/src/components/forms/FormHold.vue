<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="canIdInputGroup"
                    label="Can ID:"
                    label-for="canIdInput"
                    horizontal>
        <b-form-input id="canIdInput"
                      type="text"
                      v-model="hold.can_id"
                      required
                      placeholder="Enter can ID">
        </b-form-input>
      </b-form-group>
      <b-form-group id="distFromSxInputGroup"
                    label="Dist from left:"
                    label-for="distFromSxInput"
                    horizontal>
        <b-form-input id="distFromSxInput"
                      type="number"
                      v-model="hold.dist_from_sx"
                      required
                      placeholder="Enter distance from left edge (in cm)">
        </b-form-input>
      </b-form-group>
      <b-form-group id="distFromBotInputGroup"
                    label="Dist from bottom:"
                    label-for="distFromBotInput"
                    horizontal>
        <b-form-input id="distFromBotInput"
                      type="number"
                      v-model="hold.dist_from_bot"
                      required
                      placeholder="Enter distance from bottom (in cm)">
        </b-form-input>
      </b-form-group>
      <b-form-group id="holdTypeInputGroup"
                    label="Hold type:"
                    label-for="holdTypeInput"
                    horizontal>
        <b-form-input id="holdTypeInput"
                      type="text"
                      v-model="hold.hold_type">
        </b-form-input>
      </b-form-group>
      <b-form-group id="wallIdInputGroup"
                    label="Wall ID:"
                    label-for="wallIdInput"
                    horizontal>
        <b-form-select id="wallIdInput"
                      :options="wallIds"
                      v-model="hold.wall_id">
          <template slot="first">
            <option :value="undefined">-- No wall --</option>
          </template>
        </b-form-select>
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
    initialHold: Object,
    wallIds: Array
  },
  data () {
    return {
      show: true
    }
  },
  computed: {
    hold () {
      return Vue.util.extend({}, this.initialHold)
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('submit-hold', this.hold)
    },
    onReset (evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.hold.can_id = this.initialHold.can_id
      this.hold.dist_from_sx = this.initialHold.dist_from_sx
      this.hold.dist_from_bot = this.initialHold.dist_from_bot
      this.hold.hold_type = this.initialHold.hold_type
      this.hold.wall_id = this.initialHold.wall_id
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  }
}
</script>
