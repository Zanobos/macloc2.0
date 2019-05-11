<template>
  <div>
    <form-hold v-bind:initialHold="{}" v-bind:wallIds="wallIds" v-on:submit-hold="onSubmitHold"></form-hold>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import FormHold from '@/components/forms/FormHold.vue'

export default {
  components: {
    FormHold
  },
  computed: {
    ...mapGetters({
      wallIds: 'walls/wallIds'
    })
  },
  methods: {
    onSubmitHold (hold) {
      this.createHold(hold)
    },
    ...mapActions({
      createHold: 'holds/createHold',
      fetchWalls: 'walls/fetchWalls'
    })
  },
  created () {
    this.fetchWalls()
  }
}
</script>
