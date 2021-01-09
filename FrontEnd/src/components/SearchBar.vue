<template>
  <div class="searchBar-wrapper">
        <transition name="el-fade-in-linear">
        <form v-show="show" class="searchBar-form" @submit="SearchQuery">
            <input class="searchInput" type="search" v-model="title" placeholder="请输入搜索内容">
            <button class="searchSubBTN" type="submit" value="submit"></button>
        </form>
        </transition>
    </div>
</template>

<script>
    export default {
        name: 'SearchBar',
        props: {
            searchContent: {
                type: String,
                default: () => ''
            }
        },
        data() {
            return {
                title: this.searchContent,
                show: false
            }
        },
        mounted() {
            this.show = !this.show
        },
        methods: {
            SearchQuery() {
                // e.preventDefault();
                //send up to parent
                this.$emit('search-query', this.title);
                // this.title = '';
                // console.log("输出搜索内容", this.title)
                this.$router.push({
                    path: '/query_result',
                    query: {
                        search_content: this.title
                    }
                });
            }
        },
        watch: {
            "searchContent": {
                handler(content) {
                    this.title = content;
                }
            },
        }
    }
</script>

<style>
    div.searchBar-wrapper {
        position: relative;
        width: 70%;
        height: 100%;
        margin: auto;
    }
    
    form.searchBar-form {
        position: relative;
        width: 100%;
        height: 100%;
        margin: 0 auto;
    }
    
    input.searchInput {
        width: 100%;
        height: 45px;
        padding: 0;
        font-size: 20px;
        position: relative;
        border: 2px solid #7BA7AB;
        border-radius: 5px;
        background: #F9F0DA;
        opacity: 0.65;
        color: #9E9C9C;
    }
    
    form.searchBar-form input:focus {
        opacity: 1.0;
    }
    
    button.searchSubBTN {
        height: 45px;
        width: 45px;
        cursor: pointer;
        position: absolute;
        border: 2px solid #7BA7AB;
        top: 0;
        right: 0;
        /* background: #7BA7AB; */
        background: url(../assets/search.svg);
        background-repeat: no-repeat;
        background-position: 50% 50%;
        background-color: #7BA7AB;
        border-radius: 0 5px 5px 0;
    }
</style>