<template>
  <b-container>
    <b-row class="mt-2">
      <b-col>
        <insert-wall></insert-wall>
      </b-col>
      <b-col>
        <list-walls></list-walls>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ListWalls from '@/components/collections/ListWalls.vue'
import InsertWall from '@/components/subpages/InsertWall.vue'

export default {
  name: 'WallsPage',
  components: {
    ListWalls,
    InsertWall
  }
}
</script>
