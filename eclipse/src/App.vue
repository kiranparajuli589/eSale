<template>
  <div id="app">
    <Navbar/>
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
</style>
