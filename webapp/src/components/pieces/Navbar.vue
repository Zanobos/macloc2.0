<template>
  <div id="navbar">
    <b-navbar toggleable="md" type="light" variant="light">
      <b-nav-toggle target="nav_collapse"></b-nav-toggle>
      <b-navbar-brand>
        <img src="/static/logo_green.png" alt="Macloc">
      </b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav class="ml-auto">
          <b-nav-item v-for="route in routes" :key="route.name" :to="route">{{ route.label }}</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
  computed: {
    routes: function () {
      var routes = []
      for (var i in this.$router.options.routes) {
        if (!this.$router.options.routes.hasOwnProperty(i)) {
          continue
        }
        var route = this.$router.options.routes[i]
        if (route.hasOwnProperty('label') && !route.hasOwnProperty('hidden')) {
          routes.push(route)
        }
      }
      return routes
    }
  }
}
</script>
