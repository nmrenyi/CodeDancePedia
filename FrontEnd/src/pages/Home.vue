<template>
  <!-- 搜索页主部分 -->
    <div class="mainPage" id="home">
        <canv></canv>
            <!-- 菜单栏 -->
            <navBar></navBar>

            <!-- logo栏 -->
            <div class="logoBar">
                <div class="logoName">CodeDancePedia</div>
            </div>

            <!-- 搜索框栏 -->
            <div class="searchBar-container">
                <div class="searchBar-wrapper">
                    <searchBar v-on:search-query="searchQuery"></searchBar>
                </div>
            </div>
    </div>
</template>

<script>
    import searchBar from '../components/SearchBar'
    import navBar from '../components/NavBar'
    import canv from "../components/Canvas"
    import API from "@/utils/API"

    export default {
        name: 'home',
        components: {
            searchBar,
            navBar,
            canv
        },
        methods: {
            searchQuery(newQuery) {
                console.log(API.GET_ASK_FOR_ANSWER.path)
                console.log("in home " + newQuery)
                this.$bus.$emit('SerchQueryFromHome', newQuery)
            }
        },
    }
</script>
<style>
    * {
        margin: 0;
    }
    
    div.mainPage {
        width: 100%;
        height: 800px;
        background-color: black;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: fixed;
        /* 之后要在下面加东西的话需要把这一行去掉 */
    }
    
    div.mainPageContent {
        width: 100%;
        height: 100%;
    }
    /*********** logo栏 ************/
    
    div.logoBar {
        position: relative;
        width: 100%;
        height: 40%;
    }
    
    div.logoName {
        width: 100%;
        position: absolute;
        bottom: 5%;
        text-align: center;
        color: white;
        font-size: 40pt;
    }
    /*********** 搜索框栏 ************/
    
    div.searchBar-container {
        width: 100%;
        height: 60px;
        padding: 0 0;
        margin: auto;
        align-content: center;
    }
</style>