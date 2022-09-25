<template>
  <v-main>
    <v-container style="max-width: 960px;">
      <v-card class="mb-4 pa-2" elevation="0">
        <v-row justify="center">
          <v-card class="my-4 pa-2" elevation="0">
            <div class="d-flex justify-space-between">
              <v-btn class="ml-2" @click="refresh">Refresh</v-btn>
              <CreatePost :refresh="refresh" />
            </div>
          </v-card>
        </v-row>
        <v-row>
          <v-col>
            <ViewPostList ref="ViewPostList" />
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>

import CreatePost from './CreatePost.vue'
import ViewPostList from './ViewPostList.vue'

export default {
  name: 'MainView',
  components: {
    CreatePost,
    ViewPostList,
  },
  methods: {
    refresh() {
      this.$refs.ViewPostList.refreshElements()
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
