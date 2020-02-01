<template>
  <div id="app">
    <Navbar/>
<<<<<<< HEAD
=======
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
>>>>>>> Added navbar component
    <router-view/>
  </div>
</template>

<script>
  import Navbar from "./components/Navbar"
<<<<<<< HEAD

=======
>>>>>>> Added navbar component
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
<<<<<<< HEAD
  .page-title {
    color: #1b8db8;
    padding-top: 20px;
    border-bottom: 2px solid #17a2b8;
    margin-bottom: 20px;
    font-family: "Noto Sans Mono CJK KR";
  }
  span, label {
    font-family: FontAwesome;
  }
  .container {
    margin-left: auto;
    margin-right: auto;
  }
=======
>>>>>>> Added navbar component
</style>
