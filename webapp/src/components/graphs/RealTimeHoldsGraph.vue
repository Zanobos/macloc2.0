
<template>
  <div id="wall"
      :style="{ 'background-image': 'url(\'' + getOngoingWallImg()+ '\')' }">
  </div>
</template>

<script>
/* globals window, requestAnimationFrame */
import * as d3 from 'd3'
import { mapState, mapGetters } from 'vuex'
import { getWallImg } from '@/api'

export default {
  props: {
    wallId: Number
  },
  data () {
    return {
      svgContainer: {}
    }
  },
  computed: {
    ...mapState({
      rtholds: state => state.realtime.rtholds
    }),
    ...mapGetters({
      getForceByHoldId: 'realtime/getForceByHoldId',
      ongoingClimb: 'realtime/ongoingClimb'
    }),
    holds () {
      return this.ongoingClimb(this.wallId) === undefined ||
              this.ongoingClimb(this.wallId).holds === undefined ? []
        : this.ongoingClimb(this.wallId).holds
    },
    graphicHolds: function () {
      var graphicHolds = this.holds.map(hold => {
        var graphicHold = {}
        var percentFromBottom = hold.dist_from_bot / this.ongoingClimb(this.wallId).height * 100.0
        graphicHold.percentFromTop = 100.0 - percentFromBottom
        graphicHold.percentFromLeft = hold.dist_from_sx / this.ongoingClimb(this.wallId).width * 100.0
        graphicHold.forceFromTop = graphicHold.percentFromTop + this.getForceByHoldId('y', hold.id) / 30.0
        graphicHold.forceFromLeft = graphicHold.percentFromLeft + this.getForceByHoldId('x', hold.id) / 30.0
        return graphicHold
      })
      return graphicHolds
    }
  },
  watch: {
    rtholds: {
      handler: function (val, oldVal) {
        // Has to explicitly update the canvas
        this.drawForces()
      },
      deep: true
    },
    graphicHolds: {
      handler: function (val, oldVal) {
        // Has to explicitly update the canvas
        this.drawHolds()
        this.drawForces()
      },
      deep: true
    }
  },
  methods: {
    getOngoingWallImg () {
      return getWallImg(this.ongoingClimb(this.wallId).img)
    },
    drawWall () {
      // same height and width of the wall
      this.svgContainer = d3.select('#wall')
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
      // Adding the definition of the arrowhead
      var defs = this.svgContainer.append('defs')
      var marker = defs.append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 5)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
      marker.append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('class', 'arrowHead')
    },
    drawHolds () {
      // Joining data
      var circle = this.svgContainer.selectAll('circle')
        .data(this.graphicHolds)
      // Removing old data
      circle.exit().remove()
      // New data and update of existing
      circle.enter()
        .append('circle')
        .merge(circle)
        .attr('cx', d => d.percentFromLeft + '%')
        .attr('cy', d => d.percentFromTop + '%')
        .attr('r', 40)
        .style('fill', 'green')
    },
    drawForces () {
      // Joining data
      var line = this.svgContainer.selectAll('line')
        .data(this.graphicHolds)
      // Removing old data
      line.exit().remove()
      // New data and update of existing
      line.enter()
        .append('line')
        .merge(line)
        .attr('x1', d => d.percentFromLeft + '%')
        .attr('y1', d => d.percentFromTop + '%')
        .transition()
        .attr('x2', d => d.forceFromLeft + '%')
        .attr('y2', d => d.forceFromTop + '%')
        .attr('stroke', 'black')
        .attr('stroke-width', 4)
        .attr('class', 'arrow')
        .attr('marker-end', 'url(#arrow)')
      // Joining data
      var circle = this.svgContainer.selectAll('circle')
        .data(this.graphicHolds)
      // Removing old data
      circle.exit().remove()
      // New data and update of existing
      circle.enter()
        .append('circle')
        .merge(circle)
        .style('fill', 'green')
    }
  },
  mounted () {
    this.drawWall()
    this.drawHolds()
    this.drawForces()
  }
}
</script>

<style scoped>
  #wall {
    width: 100%;
    height: 100%;
  }
</style>
