<template>
    <v-card class="mb-4 pa-2" elevation="2" outlined>
        <v-card-title>{{ title }}</v-card-title>
        <v-img :src="img" class="d-flex" />
    </v-card>
</template>

<script>

export default {
    name: 'ViewPost',
    props: {
        id: String,
        title: String,
        img: Object
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
