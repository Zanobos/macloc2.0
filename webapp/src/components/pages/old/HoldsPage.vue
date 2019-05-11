<template>
  <b-container>
    <b-row class="mt-2">
      <b-col>
        <insert-hold></insert-hold>
      </b-col>
      <b-col>
        <list-holds></list-holds>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ListHolds from '@/components/collections/ListHolds.vue'
import InsertHold from '@/components/subpages/InsertHold.vue'

export default {
  name: 'HoldsPage',
  components: {
    ListHolds,
    InsertHold
  }
}
</script>
