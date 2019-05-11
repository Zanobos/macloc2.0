<template>
  <div>
    <b-card v-for="climb in climbs" :key="climb.id" no-body class="mb-1">
      <b-card-body>
        <b-row>
          <b-col>
            <p class="card-text" style="text-align: left">
              <ul>
                <li>Climb #{{climb.id}}</li>
                <li>Climber: {{ climb.climber_name }} </li>
                <li>Date: {{climb.start_time}} </li>
                <li>Wall grade: {{climb.wall_grade}} </li>
              </ul>
            </p>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'ListClimbs',
  computed: mapState({
    climbs: state => state.climbs.climbs
  }),
  methods: {
    ...mapActions({
      fetchClimbs: 'climbs/fetchClimbs'
    })
  },
  created () {
    this.fetchClimbs({ status: 'end' })
  }
}
</script>
