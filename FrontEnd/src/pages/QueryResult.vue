<template>
  <!--<img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to MyMy Vue.js App"/>-->
  <div class="queryPage" id="query_result">
    <canv></canv>
    <div class="searchPageContent">
    <!-- 菜单栏 -->
    <navBar style="z-index: 1000"/>

    <!-- 搜索栏 -->
    <div class="searchBar-container">
        <div class="searchBar-wrapper">
            <el-container class="searchBar-fixed">
                <searchBar style="margin:10px" v-on:search-query="searchQuery" v-bind:searchContent="search_content"></searchBar>
            </el-container>
        </div>
    </div>

    <!-- <div class="background"></div> -->

    <div class="Text-empty-container" v-if="AnswerIsEmpty === true" style="color: #cccccc">啊，这个问题我不会，很抱歉</div>
    <div v-else>
        <!-- 搜索结果展示list -->
        <div class="Texts-container">
            <p class="time_and_credit" style="color: #cccccc; font-size: 14px; margin: 5px">搜索耗时：{{time_cost}}</p>
            <p v-if="Credit === false" style="color: #cccccc; font-size: 14px; margin: 3px;">本次搜索结果可信程度较低，仅供参考。</p>
            <Texts v-bind:texts="texts"/>
        </div>
    </div>
   </div>
   
   <!--错误提示alertDialog-->
   <div>
        <el-dialog
            :name="el-dialog"
            style="text-align: center; position: absolute; top:30%"
            :append-to-body="true" 
            :title="alertDialog.text"
            :visible.sync="alertDialog.dialogVisible"
            @close='closeDialog'
            width="40%">
        </el-dialog>
   </div>
   
</div>
</template>

<script scoped>
    import NavBar from '../components/NavBar.vue'
    import SearchBar from '../components/SearchBar.vue'
    import Texts from '../components/Texts.vue'
    import API from "@/utils/API"
    import canv from "../components/Canvas"
    import {
        fetch
    } from '@/utils/communication'
    import Cookies from "@/utils/cookies"

    export default {
        name: 'QueryResult',
        components: {
            NavBar,
            SearchBar,
            Texts,
            canv
        },
        mounted() {
            this.searchQuery(this.$route.query.search_content)
        },
        data() {
            return {
                // the news searched
                texts: [],
                search_content: this.$route.query.search_content,
                alertDialog: {
                    text: "",
                    dialogVisible: false
                },
                logo_url : require('@/assets/logo.png')
            }
        },
        methods: {
            QueryResponse(response) {
                if (response.status == 500) {
                    this.texts = []
                    this.AnswerIsEmpty = false
                    console.log("status = " + response.status)
                    this.alertDialog.text = "连接到服务器错误"
                    this.alertDialog.dialogVisible = true
                } else if (response.status == 400) {
                    this.texts = []
                    this.AnswerIsEmpty = true
                } else if (response.status != 200) {
                    this.texts = []
                    this.AnswerIsEmpty = false
                    console.log("status = " + response.status)
                    this.alertDialog.text = "请求错误，请重试"
                    this.alertDialog.dialogVisible = true
                } else {
                    this.texts = []
                    this.AnswerIsEmpty = false
                    this.time_cost = response.data.time
                    this.texts = response.data.data
                    this.Credit = (response.data.data[0].credit == 0) ? false : true;
                    console.log(response.data.data[0].credit)
                    for (var text of this.texts) {
                        text.doc_id = "【文档 id: " + text.doc_id + "】"
                    }
                }
                this.$forceUpdate()
            },
            QueryError(err) {
                this.texts = []
                this.AnswerIsEmpty = false
                console.log("err = " + err)
                this.alertDialog.text = "请求错误，请重试"
                this.alertDialog.dialogVisible = true
            },
            searchQuery(newQuery) {
                console.log(API.GET_ASK_FOR_ANSWER.path)
                console.log("I'm doing some search: ", newQuery)
                fetch(API.GET_ASK_FOR_ANSWER.path, {
                    ask: newQuery,
                    username: Cookies.getCookie("username"),
                    user_id: Cookies.getCookie("user_id")
                }, "搜肠刮肚思考回答中...").then(response => {
                    this.QueryResponse(response)
                }).catch(err => {
                    this.QueryError(err)
                })
                this.$forceUpdate()
            },
            closeDialog: function() {
                this.alertDialog.dialogVisible = false
            }
        }
    }
</script>

<style scoped>
    * {
        background-color: rgb(0, 0, 0, 0);
    }
    
    div.queryPage {
        background-color: black;
    }
    
    div.searchBar-container {
        position: fixed;
        top: 75px;
        width: 100%;
        margin: 5px;
        z-index: 100;
    }
    
    div.searchBar-wrapper {
        width: 70%;
        position: absolute;
        left: 15%;
        bottom: 5%;
        align-self: center;
        padding: 0 0;
        margin: auto;
    }
    
    div.Text-empty-container {
        position: fixed;
        top: 154px;
        width: 100%;
        height: 100%;
        padding-bottom: 124px;
        align-self: center;
        align-content: center;
        font-size: large;
    }
    
    div.Texts-container {
        position: fixed;
        top: 124px;
        width: 100%;
        height: 100%;
        padding-bottom: 124px;
        /* margin-bottom: 124px; */
        /* margin: auto; */
        overflow: scroll;
        align-self: center;
        align-content: center;
    }
    
    div.Texts-container::-webkit-scrollbar {
        display: none;
    }
</style>