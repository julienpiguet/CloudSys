<template>
    <v-footer padless>
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} — <strong>HES-SO Master</strong>
      </v-col>
    </v-footer>
  </template>
  
  <script>
  
  export default {
    name: 'FooterBar'
  }
  
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  </style>
  