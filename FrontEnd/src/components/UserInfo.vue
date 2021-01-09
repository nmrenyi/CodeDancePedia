<template>
<div style="width:80%; margin:auto">
    <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="用户名">
            <el-input v-model="form.username"></el-input>
            <div v-if="username_valid===false" style="color: red">请检查用户名：不能有空格、开头不能是数字和奇怪的字符噢~</div>
        </el-form-item>
        <el-form-item label="个性签名">
            <el-input v-model="form.bio" placeholder="一句话描述一下你自己吧~"></el-input>
        </el-form-item>
        <el-form-item label="密码">
            <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" v-show="show_confirm">
            <el-input type="password" v-model="form.confirm_password"></el-input>
            <div v-if="password_valid===false" style="color: red">请保证与输入密码一致</div>
        </el-form-item>
        <el-form-item>
            <el-button type="success" :disabled="!(((valid)||(password_valid))&&(username_valid))" @click="onSubmit">修改信息</el-button>
            <el-button @click="reset">取消</el-button>
        </el-form-item>
    </el-form>
</div>
</template>


<script>
    import {
        post
    } from '@/utils/communication'
    import API from "@/utils/API"
    import Cookies from "@/utils/cookies"

    export default {
        name: 'UserInfo',
        mounted() {
            this.reset()
        },
        props: {
            username: {
                type: String,
                default: () => ""
            },
            bio: {
                type: String,
                default: () => ""
            },
            password: {
                type: String,
                default: () => ""
            },
            user_id: {
                default: () => -1
            }
        },
        data() {
            return {
                form: {
                    username: '',
                    bio: '',
                    password: '',
                    confirm_password: '',
                    user_id: 0
                },
                show_confirm: false,
                password_valid: false,
                username_valid: false,
                valid: true,
            }
        },
        methods: {
            submitResponse(response) {
                console.log("文档返回内容", response)
                if (response.status == 200) {
                    this.$message({
                        type: 'success',
                        message: '用户信息修改成功'
                    });
                    var data = JSON.parse(response.data.data)
                    this.form.username = data.username
                    this.form.user_id = data.user_id
                    this.form.bios = data.bios
                    Cookies.setCookie('username', data.username, 1)
                    Cookies.setCookie('user_id', data.user_id, 1)
                    this.$emit('userinfo', this.form)
                } else {
                    this.$message({
                        type: 'error',
                        message: '用户信息修改失败：' + response.data.data
                    });
                }
            },
            onSubmit() {
                console.log('submit!');
                post(API.POST_USER_INFO.path, this.form).then(response => {
                    this.submitResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
            },
            reset() {
                this.form.username = this.username
                this.form.user_id = this.user_id
                this.form.bio = this.bio
                this.form.password = this.password
                this.form.confirm_password = ''
                this.show_confirm = false
                this.valid = true
            }
        },
        watch: {
            "form.password": {
                handler() {
                    if (this.form.password != this.password) {
                        this.show_confirm = true
                        this.valid = false
                    }
                    if (this.form.password != this.form.confirm_password) {
                        this.password_valid = false
                    } else {
                        this.password_valid = true
                    }
                }
            },
            "form.confirm_password": {
                handler() {
                    if (this.form.password != this.form.confirm_password) {
                        this.password_valid = false
                    } else {
                        this.password_valid = true
                    }
                }
            },
            "form.username": {
                handler(inputName) {
                    this.username_valid = /^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(inputName)
                }
            },
            "user_id": {
                handler() {
                    this.reset()
                }
            }
        }
    }
</script>

<style scoped>

</style>