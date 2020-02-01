<template>
  <div id="app">
    <Navbar/>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
    <router-view/>
  </div>
</template>

<script>
  import Navbar from "./components/Navbar"
  export default {
    name: 'App',
    components: {
      Navbar
    },
  }
</script>

<style>
  /*universal styles*/
  a {
    font-family: "Ubuntu Condensed";
    color: #4091e2
  }
</style>
