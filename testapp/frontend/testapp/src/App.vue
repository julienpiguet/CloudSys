<template>
  <v-app>
    <HeaderBar />
    <MainView/>
    <FooterBar />
  </v-app>
</template>

<script>
import FooterBar from './components/FooterBar.vue'
import HeaderBar from './components/HeaderBar.vue'
import MainView from './components/MainView.vue'



export default {
  name: 'App',

  components: {
    HeaderBar,
    FooterBar,
    MainView
  },


  data: () => ({
    //
  }),
}
</script>
