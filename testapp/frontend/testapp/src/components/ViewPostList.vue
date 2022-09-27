<template>
    <v-card class="mb-4" elevation="0">
        <v-row v-for="item in itemList.reverse()" :key="item.id">
            <v-col>
                <ViewPost :id="item.id" :title="item.title" :img="item.img"/>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
import { API_LOCATION } from "../config"
import ViewPost from './ViewPost.vue'

export default {
    name: 'ViewPostList',

    components: {
        ViewPost
    },

    

    data: () => ({
        itemList: [],
    }),

    methods: {
        refreshElements() {
            const requestOptions = {
                method: "GET",
            };
            fetch(API_LOCATION+"/element/all", requestOptions)
                .then(response => response.json())
                .then(data => (this.itemList = data.data));
            console.log(this.itemList)
        },
    },

    created()  {
        this.refreshElements()
    },
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
