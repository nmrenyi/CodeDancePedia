<template>
    <div>
        <el-card style="margin-bottom: 10px">
        <el-steps :align-center="true" :active="active" finish-status="success">
            <el-step title="在搜索框中输入文档编号，按回车键" ></el-step>
            <el-step title="在文本框中修改文档或【删除文档】"></el-step>
            <el-step title="点击【修改文档】或【删除文档】"></el-step>
        </el-steps>
        </el-card>
        <el-input class="search" type="search" placeholder="请输入文档编号" prefix-icon="el-icon-search" @keyup.enter.native="submitSearch" :disabled="!textDisabled" v-model="doc_id"/>
        <el-input class="edit" type="textarea" rows="14" placeholder="请输入内容" :disabled="textDisabled" v-model="textarea" @input="editChanged"/>
        <div style="margin-top: 10px">
            <el-button @click="cancel">取 消</el-button>
            <el-button type="danger" :disabled="textDisabled" @click="del">删除文档</el-button>
            <el-button type="primary" :disabled="confirmDisabled" @click="confirm">确认修改</el-button>
        </div>
    </div>
</template>

<script>
    import {
        post
    } from '@/utils/communication'
    import API from "@/utils/API"
    import Cookies from "@/utils/cookies"

    export default {
        name: 'Modify_Doc',
        data() {
            return {
                textarea: "",
                origin_text: "",
                textDisabled: true,
                confirmDisabled: true,
                doc_id: "",
                active: 0
            }
        },
        methods: {
            submitResponse(response) {
                console.log("文档返回内容", response)
                if (response.status == 200) {
                    console.log("sign in success: ", JSON.parse(response.data.data))
                    this.textDisabled = false
                    this.textarea = JSON.parse(response.data.data).content
                    this.origin_text = this.textarea
                    this.active = 1
                    this.$message({
                        type: 'success',
                        message: '文档查找成功!'
                    });
                } else {
                    console.log("文档恢复错误码：", response)
                    var error_code = JSON.parse(response.data.data).code
                    if (error_code == 7) {
                        this.$confirm('您查找的文档已经删除啦，是否恢复？', '提示', {
                            confirmButtonText: '恢复',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            this.restore()
                        })
                    } else {
                        this.$message({
                            type: 'error',
                            message: '文档查找失败：' + JSON.parse(response.data.data).detail
                        });
                    }
                    console.log("failed", response.data.data)
                }
            },
            confirmResponse(response) {
                console.log("文档返回内容", response)
                if (response.status == 200) {
                    console.log("sign in success: ", JSON.parse(response.data.data))
                    this.origin_text = this.textarea
                    this.confirmDisabled = true
                    this.active = 1
                    this.$message({
                        type: 'success',
                        message: '文档修改成功!'
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: '文档修改失败：' + JSON.parse(response.data.data).detail
                    });
                    console.log("failed", response.data.data)
                }
            },
            deleteResponse(response) {
                console.log("文档返回内容", response)
                if (response.status == 200) {
                    this.doc_id = ""
                    this.cancel()
                    this.$message({
                        type: 'success',
                        message: '文档删除成功!'
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: '文档修改失败：' + JSON.parse(response.data.data).detail
                    });
                    console.log("failed", response.data.data)
                }
            },
            // fetch document            
            submitSearch() {
                let Doc_package = {
                    username: Cookies.getCookie("username"),
                    user_id: Cookies.getCookie("user_id"),
                    document_id: this.doc_id,
                    type: "fetch"
                }
                console.log(Doc_package)
                post(API.POST_DOC_MODIFY.path, Doc_package).then(response => {
                    //console.log("文档返回内容", response)
                    this.submitResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
            },
            editChanged() {
                if (this.origin_text != this.textarea) {
                    this.confirmDisabled = false
                    this.active = 2
                } else {
                    this.confirmDisabled = true
                    this.active = 1
                }
            },
            cancel() {
                this.textarea = ""
                this.textDisabled = true
                this.confirmDisabled = true
                this.active = 0
            },
            // confirm document modify
            confirm() {
                let Doc_package = {
                    username: Cookies.getCookie("username"),
                    user_id: Cookies.getCookie("user_id"),
                    document_id: this.doc_id,
                    type: "modify",
                    content: this.textarea
                }
                console.log(Doc_package)
                post(API.POST_DOC_MODIFY.path, Doc_package).then(response => {
                    this.confirmResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
            },
            // delete document
            del() {
                this.$confirm('此操作将永久删除该文档, 是否继续?', '警告', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let Doc_package = {
                        username: Cookies.getCookie("username"),
                        user_id: Cookies.getCookie("user_id"),
                        document_id: this.doc_id,
                        type: "delete"
                    }
                    post(API.POST_DOC_MODIFY.path, Doc_package).then(response => {
                        this.deleteResponse(response)
                    }).catch(err => {
                        console.log("err = " + err)
                        this.$message.error('服务器连接异常，请检查网络:' + err)
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            // restore
            restore() {
                let Doc_package = {
                    username: Cookies.getCookie("username"),
                    user_id: Cookies.getCookie("user_id"),
                    document_id: this.doc_id,
                    type: "restore",
                }
                console.log(Doc_package)
                post(API.POST_DOC_MODIFY.path, Doc_package).then(response => {
                    this.restoreResponse(response)
                }).catch(err => {
                    console.log("err = " + err)
                    this.$message.error('服务器连接异常，请检查网络:' + err)
                })
            },
            restoreResponse(response) {
                if (response.status == 200) {
                    this.textDisabled = false
                    this.textarea = JSON.parse(response.data.data).content
                    this.origin_text = this.textarea
                    this.active = 1
                    this.$message({
                        type: 'success',
                        message: '文档恢复成功!'
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: '文档恢复失败：' + JSON.parse(response.data.data).detail
                    });
                }
            }
        }
    }
</script>

<style scoped>
    .el-input.search {
        margin-bottom: 10px;
    }
    
    .el-input.edit {
        margin-bottom: 10px;
    }
</style>