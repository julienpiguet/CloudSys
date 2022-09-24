<template>
  <v-app>
    <HeaderBar/>
    <v-main>
        <v-container style="max-width: 960px;">
          <v-card class="mb-4 pa-2" elevation="0">
            <v-row>
              <v-col>
                <CreatePost/>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <ViewPostList/>
              </v-col>
            </v-row>
          </v-card>
          </v-container>
        </v-main>
    <FooterBar/>
  </v-app>
</template>

<script>
import FooterBar from './components/FooterBar.vue'
import HeaderBar from './components/HeaderBar.vue'
import CreatePost from './components/CreatePost.vue'
import ViewPostList from './components/ViewPostList.vue'


export default {
  name: 'App',

  components: {
    HeaderBar,
    FooterBar,
    CreatePost,
    ViewPostList,
},


  data: () => ({
    //
  }),
}
</script>
