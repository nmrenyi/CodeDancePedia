<template>
    <div class="signinContainer">
      <canv></canv>
      <navBar></navBar>
      <div class="signinBar">
      <transition name="el-fade-in-linear">
      <el-card v-show="show" style="width:100%; height:90%; border-radius:20px; position:relative">
            <div slot="header" class="clearfix">
                <span>登录</span>
            </div>
            <el-form action="">
                <el-form-item style="margin-bottom: 22px;">
                    <el-container>
                    <el-input class="username_input" type="text" placeholder="请输入用户名" prefix-icon="el-icon-user" v-model="state.username"/>
                    </el-container>
                </el-form-item>
                <el-form-item style="margin-bottom: 22px;">
                    <el-container>
                    <el-input class="password_input" type="password" placeholder="请输入用户密码" prefix-icon="el-icon-lock" v-model="state.password"/>
                    </el-container>
                    <div v-if="state.username_valid===false" style="color: red">请检查用户名：不能有空格、开头不能是数字和奇怪的字符噢~</div>
                </el-form-item>
            </el-form>
            <span class="card-footer">
                        <el-button class="cancel" @click="cancel">取 消</el-button>
                        <el-button class="confirm" type="primary" @click="signin"
                        :disabled="state.username_valid===false">
                        登 录</el-button>
            </span>
            <div style="position:absolute; bottom: 5%; left: 0px; width:100%; text-align: center"><el-link type="primary" @click="to_signup">还没有账号？点击注册</el-link></div>
      </el-card>
      </transition>
        <el-dialog
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

<script>
    import navBar from '../components/NavBar'
    import canv from "../components/Canvas"
    import {
        post
    } from '@/utils/communication'
    import API from "@/utils/API"
    import Cookies from "@/utils/cookies"

    export default {
        name: 'Signin',
        components: {
            navBar,
            canv
        },
        props: {
            dialogVisible: {
                type: Boolean,
                default: () => true
            },
            state: {
                type: Object,
                default: () => {
                    return {
                        username: "",
                        username_valid: false,
                        password: "",
                    }
                }
            },
        },
        data() {
            return {
                show: false,
                alertDialog: {
                    text: "登录成功",
                    dialogVisible: false,

                },
            }
        },
        methods: {
            cancel: function() {
                console.log("cookie: ", document.cookie)
                this.$router.push('/')
            },
            signinResponse(response) {
                console.log("用户登录返回信息", response)
                if (response.status != 200) { //failed
                    this.alertDialog.text = "登录失败: " + response.data.data
                    this.alertDialog.dialogVisible = true
                } else { //sucess
                    console.log("sign in success: ", JSON.parse(response.data.data).username)
                    Cookies.setCookie("username", JSON.parse(response.data.data).username, 1)
                    Cookies.setCookie("user_id", JSON.parse(response.data.data).user_id, 1)
                    this.alertDialog.text = "登录成功"
                    this.alertDialog.dialogVisible = true
                }
            },
            signin: function() {
                let userData = {
                    username: this.state.username,
                    password: this.state.password
                }
                console.log("登录信息：", userData)
                post(API.POST_USER_SIGNIN.path, userData).then(response => {
                    this.signinResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                    this.texts = []
                })
            },
            closeDialog: function() {
                this.$router.push('/')
            },
            to_signup: function(){
                this.$router.push('/sign_up')
            }
        },
        mounted() {
            this.show = !this.show
        },
        watch: {
            "state.username": {
                handler(inputName) {
                    this.state.username_valid = /^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(inputName)
                }
            },
        }
    }
</script>

<style scoped>
    * {
        margin: 0;
    }
    
    div.signinContainer {
        width: 100%;
        height: 100%;
        position: fixed;
        background-color: black;
    }
    
    div.signinBar {
        width: 36%;
        height: 70%;
        left: 32%;
        top: 120px;
        position: fixed;
        justify-content: center;
        display: flex;
    }
</style>