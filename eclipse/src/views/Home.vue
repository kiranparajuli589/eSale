<template>
  <div class="home">
    <Navbar/>
    <Item/>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '../components/Navbar.vue'
import Item from "../components/Item"

export default {
  name: 'home',
  components: {
    Navbar,
    Item,
  }
}
</script>
