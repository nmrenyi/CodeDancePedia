<template>
    <div style="position: relative">
        <canv/>
        <navBar/>
        <el-container>
            <el-header style="height:0"></el-header>
            <el-main>
                <div class="about_title">About CodeDance</div>
                <div class="introduction"><p style="margin-left:20px; margin-right:20px">{{introduction}}</p></div>
                <div class="show_pic">
                <el-carousel class="pic_carousel" type="card" :interval=3000>
                    <el-carousel-item v-for="(img,index) in imgList" :key="index">
                        <img :src="img.url" width="100%" height="100%">
                    </el-carousel-item>
                </el-carousel>
                </div>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import navBar from '../components/NavBar'
import canv from "../components/Canvas"

export default {
    name: 'home',
    components: {
        navBar,
        canv
    },
    data(){
        return{
            imgList:[
            {url:require('@/assets/group1.jpg')},
            {url:require('@/assets/group2.jpg')},
            {url:require('@/assets/group3.jpg')},
            {url:require('@/assets/group4.jpg')},
            ],
            introduction:"本项目是2020年秋季学期软件工程课程项目，开发人员是（按学号顺序）潘传宇、邹恬圆、刘畅、戴傲初、任一。项目主体功能是智能问答，即处理用户输入的问题，针对问题检索得到相关的文档，并用机器阅读理解模型从文档中抽取答案返回给用户。此外，本项目还具有用户管理、文档增删改、保存搜索历史记录等功能。",
        }
    }
}
</script>

<style scoped>
    .el-carousel.pic_carousel{
        position: relative;
        margin: auto;
        width: 990px;
    }

    .el-container{
        position: fixed;
        top: 70px;
    }

    div.about_title{
        position: relative;
        color: azure;
        font-family: "Georgia", Tahoma, Sans-Serif;
        font-size: 25pt;
    }

    div.introduction{
        position: relative;
        margin: 25px;
        left: 20%;
        width: 60%;
        text-align: left;
        color: azure;
        font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;
        border-left: 2px solid azure;
    }

    div.show_pic{
        position: relative;
    }

    img{
        border-radius: 10px;
    }
</style>