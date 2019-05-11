<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="gradeInputGroup"
                    label="Wall grade:"
                    label-for="gradeInput"
                    horizontal>
        <b-form-input id="gradeInput"
                      type="text"
                      v-model="wall.grade"
                      required
                      placeholder="Enter grade">
        </b-form-input>
      </b-form-group>
      <b-form-group id="heightInputGroup"
                    label="Height:"
                    label-for="heightInput"
                    horizontal>
        <b-form-input id="heightInput"
                      type="number"
                      v-model="wall.height"
                      required
                      placeholder="Enter height (in cm)">
        </b-form-input>
      </b-form-group>
      <b-form-group id="widthInputGroup"
                    label="Width:"
                    label-for="widthInput"
                    horizontal>
        <b-form-input id="widthInput"
                      type="number"
                      v-model="wall.width"
                      required
                      placeholder="Enter width (in cm)">
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
    initialWall: Object
  },
  data () {
    return {
      show: true
    }
  },
  computed: {
    wall () {
      return Vue.util.extend({}, this.initialWall)
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('submit-wall', this.wall)
    },
    onReset (evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.wall.grade = this.initialWall.grade
      this.wall.height = this.initialWall.height
      this.wall.width = this.initialWall.width
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  }
}
</script>
