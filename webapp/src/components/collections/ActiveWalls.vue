<template>
  <b-carousel id="carousel1"
    style="text-shadow: 1px 1px 2px #333; max-height: inherit;"
    class="d-block"
    controls
    indicators
    background="#ababab"
    :interval="0"
    v-model="slide"
    @sliding-start="onSlideStart"
    @sliding-end="onSlideEnd"
  >
    <b-carousel-slide v-for="wall in walls" :key="wall.id" img-blank>

      <climb-ongoing :wallId="wall.id"></climb-ongoing>

    </b-carousel-slide>
  </b-carousel>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import ClimbOngoing from '@/components/subpages/ClimbOngoing'

export default {
  components: {
    ClimbOngoing
  },
  data () {
    return {
      slide: 0,
      sliding: null
    }
  },
  computed: {
    ...mapState({
      walls: state => state.walls.walls,
      climbs: state => state.realtime.ongoingClimbs
    }),
    ...mapGetters({
      ongoingClimb: 'realtime/ongoingClimb'
    })
  },
  methods: {
    onSlideStart (slide) {
      this.sliding = true
    },
    onSlideEnd (slide) {
      this.sliding = false
    },
    ...mapActions({
      fetchWalls: 'walls/fetchWalls',
      getOngoingClimbs: 'realtime/getOngoingClimbs',
      fetchUsers: 'users/fetchUsers'
    })
  },
  created () {
    this.fetchWalls()
    this.getOngoingClimbs()
    this.fetchUsers()
  }
}
</script>

<style>
.carousel-inner {
  max-height: inherit;
}
.carousel-item {
  max-height: inherit;
}
</style>
