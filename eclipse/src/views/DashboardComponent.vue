<template>
  <div class="container">
    <Item/>
  </div>
</template>

<script>
// @ is an alias to /src
import Item from "../components/Item"

export default {
  name: 'Home',
  components: {
    Item,
  }
}
</script>
