<template>
    <div class="signinContainer">
      <canv></canv>
      <navBar></navBar>
      <div class="signinBar">
      <transition name="el-fade-in-linear">
      <el-card v-show="show" style="width:100%; height:100%; border-radius:20px">
            <div slot="header" class="clearfix">
                <span>注册</span>
            </div>
            <el-form action="">
                <el-form-item style="margin-bottom: 22px;">
                    <el-container>
                    <el-input type="text" placeholder="请输入用户名" prefix-icon="el-icon-user" v-model="state.username"/>
                    </el-container>
                </el-form-item>
                <el-form-item style="margin-bottom: 22px;">
                    <el-container>
                    <el-input type="password" placeholder="请输入用户密码" prefix-icon="el-icon-lock" v-model="state.password"/>
                    </el-container>
                </el-form-item>
                <el-form-item style="margin-bottom: 22px;">
                    <el-container>
                    <el-input type="password" placeholder="请再次输入用户密码" prefix-icon="el-icon-lock" v-model="state.confirm_password"/>
                    </el-container>
                    <div v-if="state.username_valid===false" style="color: red">请检查用户名：不能有空格、开头不能是数字和奇怪的字符噢~</div>
                    <div v-if="state.password_valid===false" style="color: red">两次输入的密码不一致噢~</div>
                </el-form-item>
            </el-form>
            <span class="card-footer">
                        <el-button class="cancel" @click="cancel">取 消</el-button>
                        <el-button class="register" type="primary" @click="signup"
                         :disabled="state.username_valid===false || state.password_valid==false || state.password==''">
                        注 册</el-button>
            </span>
            <div style="position:absolute; bottom: 5%; left: 0px; width:100%; text-align: center"><el-link type="primary" @click="to_signin">已有账号？点击登录</el-link></div>
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
    import {
        post
    } from '@/utils/communication'
    import API from "@/utils/API"
    import Cookies from "@/utils/cookies"
    import canv from "../components/Canvas"

    export default {
        name: 'Signup',
        components: {
            navBar,
            canv
        },
        props: {
            state: {
                type: Object,
                default: () => {
                    return {
                        username: "",
                        username_valid: false,
                        password: "",
                        confirm_password: "",
                        password_valid: true
                    }
                }
            },
        },
        data() {
            return {
                show: false,
                alertDialog: {
                    text: "注册成功",
                    dialogVisible: false,

                },
            }
        },
        mounted() {
            this.show = !this.show
        },
        methods: {
            cancel: function() {
                console.log("cookie: ", document.cookie)
                this.$router.push('/')
            },
            signupResponse(response) {
                console.log("用户注册返回信息", response)
                if (response.status == 200) {
                    console.log("sign up success: ", JSON.parse(response.data.data).username)
                    Cookies.setCookie("username", JSON.parse(response.data.data).username, 1)
                    Cookies.setCookie("user_id", JSON.parse(response.data.data).user_id, 1)
                    this.alertDialog.text = "注册成功"
                    this.alertDialog.dialogVisible = true
                } else {
                    this.alertDialog.text = "注册失败: " + response.data.data
                    this.alertDialog.dialogVisible = true
                }
            },
            signup: function() {
                var userData = {
                    username: this.state.username,
                    password: this.state.password,
                    password_confirmed: this.state.confirm_password,
                }
                console.log("注册信息：", userData)
                post(API.POST_USER_SIGNUP.path, userData).then(response => {
                    this.signupResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
            },
            closeDialog: function() {
                this.$router.push('/')
            },
            to_signin: function() {
                this.$router.push('/sign_in')
            }
        },
        watch: {
            "state.confirm_password": {
                handler(confirmed_pw) {
                    if (confirmed_pw != this.state.password) {
                        this.state.password_valid = false;
                    } else this.state.password_valid = true;
                }
            },
            "state.password": {
                handler(pw) {
                    if (pw != this.state.confirm_password) {
                        this.state.password_valid = false;
                    } else this.state.password_valid = true;
                }
            },
            "state.username": {
                handler(inputName) {
                    this.state.username_valid = /^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(inputName)
                }
            },
        },
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
        height: 80%;
        left: 32%;
        top: 90px;
        position: fixed;
        justify-content: center;
        display: flex;
    }
</style>