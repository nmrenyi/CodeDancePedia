<template>
<div style="width: 100%; position: relative">
    <navBar style="position: relative; opacity: 1;" :name="username" v-on:label_change="label_change"/>
    <el-container style="height: 100%">
        <el-aside width="250px" height="100%" style="background-color: rgb(238, 241, 246)">
            <el-card class="block">
                <el-avatar shape="circle" :size="100" style="margin-top: 50px"> {{username}} </el-avatar>
                <div style="margin-top: 30px">{{bio}}</div>
            </el-card>
        </el-aside>
        
        <el-card style="width: 100%;" shadow='never'>
        <el-container>
            <el-header height="0px">
            </el-header>
            <el-tabs style="height: 100%;" v-model="activeTask" :stretch="stretch" type="border-card">
                <el-tab-pane label="用户管理" name="user_management"><userinfo :username="username" :bio="bio" :password="password" :user_id="user_id" v-on:userinfo="user_change"/></el-tab-pane>
                <el-tab-pane label="历史纪录" name="history"><history/></el-tab-pane>
                <el-tab-pane label="文档修改" name="doc_modify"><modifyDoc/></el-tab-pane>
                <el-tab-pane label="添加文档" name="doc_add"><uploadDoc/></el-tab-pane>
            </el-tabs>
        </el-container>
        </el-card>
    </el-container>

    <el-dialog
        style="text-align: center; position: absolute; top:15%;"
        :append-to-body="true" 
        :title="alertDialog.text"
        :visible.sync="alertDialog.dialogVisible"
        @close='closeDialog'
        width="35%">
        <span>检测到您未登录，不能查看用户界面！是否登录？</span>
        <span slot="footer" class="dialog-footer">
            <el-button @click="closeDialog">取 消</el-button>
            <el-button type="primary" @click="to_signin">确 定</el-button>
        </span>
    </el-dialog>
</div>  
</template>
<script>
    import Cookies from "@/utils/cookies"
    import navBar from '../components/NavBar'
    import history from "../components/History"
    import userinfo from "../components/UserInfo"
    import uploadDoc from "../components/Upload_Doc"
    import modifyDoc from "../components/Modify_Doc"
    import {
        fetch
    } from '@/utils/communication'
    import API from "@/utils/API"

    export default {
        name: 'user',
        components: {
            navBar,
            history,
            userinfo,
            uploadDoc,
            modifyDoc,
        },
        data() {
            return {
                username: "",
                stretch: true,
                activeTask: this.$route.params.label,
                bio: "",
                password: "",
                user_id: -1,
                alertDialog:{
                    text: "错误提示",
                    dialogVisible: false
                }
            }
        },
        methods: {
            unregister() {
                var user_id = Cookies.getCookie("user_id")
                if (user_id < 0 || user_id == '') {
                    this.alertDialog.dialogVisible = true
                }
            },
            mountFunction() {
                this.unregister()
                let cert_info = {
                    username: Cookies.getCookie("username"),
                    user_id: Cookies.getCookie("user_id")
                }
                fetch(API.POST_USER_INFO.path, cert_info, "正在获取用户信息..").then(response => {
                    if (response.status == 200) {
                        // console.log(response)
                        var data = JSON.parse(response.data.data)
                        this.username = data.username
                        this.user_id = data.user_id
                        this.bio = data.bio
                        this.password = data.password
                    } else {
                        this.$message({
                            type: 'error',
                            message: '用户信息获取失败：' + response.data.data
                        });
                    }
                }).catch(err => {
                    console.log(err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
                console.log("路由信息：", this.$route.params.label)
                if (!this.$route.params.label) this.activeTask = "user_management"
                else this.activeTask = this.$route.params.label
            },
            user_change(user_data) {
                this.username = user_data.username
                this.user_id = user_data.user_id
                this.bio = user_data.bio
                this.password = user_data.password
            },
            label_change(label) {
                this.activeTask = label
            },
            closeDialog(){
                this.$router.push('/')
            },
            to_signin(){
                this.$router.push('/sign_in')
            }
        },
        mounted() {
            this.mountFunction()
        },
    };
</script>

<style>
    * {
        margin: 0;
    }
    
    .el-header {
        background-color: #DCDFE6;
        color: #333;
        line-height: 60px;
    }
    
    .el-aside {
        color: #333;
    }
    
    .el-card.block {
        border: 0;
        height: 100%;
        width: 100%;
    }
</style>