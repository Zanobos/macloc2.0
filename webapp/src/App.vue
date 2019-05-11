<template>
  <div id="app">
    <navbar id="navbar"/>
    <div id="body">
       <router-view/>
    </div>
    <foot id="foot"/>
  </div>
</template>

<script>
import Navbar from '@/components/pieces/Navbar.vue'
import Foot from '@/components/pieces/Foot.vue'

export default {
  name: 'app',
  components: {
    Navbar,
    Foot
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#navbar {
  max-height: 20vh;
}
#body {
  height: 70vh;
  max-height: 70vh;
  background: radial-gradient(circle, #38C1B8 0%, #18A39D 77%, #1D9591 100%);
}
#footer {
  max-height: 10vh;
}
</style>
