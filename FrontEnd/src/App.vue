<template>
  <div id="app">
    <router-view></router-view>
    <!-- dkqlcekl -->
  </div>
</template>

<script>
    //import Cookies from "@/utils/cookies"

    export default {
        name: 'App',
    }
</script>

<style scoped>
    * {
        margin: 0;
    }
    
    body {
        /* height: 1200px; */
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }
    
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 0;
    }
</style>