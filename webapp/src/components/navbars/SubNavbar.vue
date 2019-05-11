<template>
  <div id="subnavbar">
    <b-nav justified pills class="mt-3">
      <b-nav-item v-for="subRoute in subRoutes" :key="subRoute.name" :to="subRoute">{{ subRoute.label }}</b-nav-item>
    </b-nav>
  </div>
</template>

<script>
export default {
  name: 'SubNavbar',
  props: {
    parentRouteLabel: String
  },
  computed: {
    subRoutes: function () {
      var subRoutes = []
      for (var i in this.$router.options.routes) {
        if (!this.$router.options.routes.hasOwnProperty(i)) {
          continue
        }
        var route = this.$router.options.routes[i]
        if (route.label === this.parentRouteLabel) {
          for (var j in route.children) {
            var subRoute = route.children[j]
            if (subRoute.hasOwnProperty('label')) {
              subRoutes.push(subRoute)
            }
          }
        }
      }
      return subRoutes
    }
  }
}
</script>
