<template>
  <div>
    <form-wall v-bind:initialWall="{}" v-on:submit-wall="onSubmitWall"></form-wall>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import FormWall from '@/components/forms/FormWall.vue'

export default {
  components: {
    FormWall
  },
  methods: {
    onSubmitWall (hold) {
      this.createWall(hold)
    },
    ...mapActions({
      createWall: 'walls/createWall'
    })
  }
}
</script>
