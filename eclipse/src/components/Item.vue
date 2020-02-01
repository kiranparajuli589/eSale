<template>
    <div id="item">
        "welcome to my items"
        <button v-on:click="getItems">All Items</button>
        <li v-for="item in items">
            {{ item.item_name }}
            {{ item.item_code }}
            {{ item.buying_rate }}
            {{ item.selling_rate }}
            {{ item.quantity }}
        </li>
    </div>
</template>

<script>
    import axios from "axios"
    export default {
        name: "Item",
        data() {
            return {
                items: [],
            }
        },
        methods: {
            getItems() {
                axios.get("http://127.0.0.1:8000/api/items/")
                .then((res) => {
                    this.items = res.data
                    console.log(this.items)
                })
                .catch(err => console.log(err))
            }
        }
    }
</script>

<style scoped>

</style>