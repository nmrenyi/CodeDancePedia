<!--<ul id="history">
        <el-tag type="info" v-for="query in queryList" :key="query">
          {{ query }}
        </el-tag>
    </ul>-->

<template>
    <div class="historyContainer" style="height: auto;">
            <div v-if="HistoryIsEmpty === true" style="color: black">历史记录空空如也</div>
            <div v-else>
                <div class="historyClearWrapper">
                    <el-button type="danger" round plain icon="el-icon-delete" @click="clearHistory">
                        清空历史记录
                    </el-button>
                </div>    
                <!-- <el-tree :data="data" :props="defaultProps"></el-tree>@node-click="handleNodeClick" -->
                <el-collapse style="align-content: center; border-color: rgba(0, 0, 0, 0)">
                    <el-card v-bind:key="question.id" v-for="question in data" class="question-card">
                        <el-collapse-item :name="question.id">
                                <div style="width: 98%; float: left;" slot="title">
                                    <p class="question" align="left" style="float: left; overflow: hidden; text-overflow:ellipsis; white-space:nowrap; width:100%;font-size: 13pt; font-weight:bold"><i class="el-icon-question" style="margin: 10px"/>{{question.label}}</p>
                                </div>
                            <el-collapse>
                                <el-collapse-item :name="doc.id" v-bind:key="doc.id" v-for="doc in question.children" style="width: 95%; position: relative; left:5%">
                                        <p slot="title" class="doc" style="float: left; font-size: 11pt"><i class="el-icon-chat-line-square" style="margin: 10px"/>{{doc.label}}</p>
                                        <p v-html="$options.filters.highlight(doc.children[0].label, doc.label)" style="text-align: left; font-size: 11pt; width: 95%; position: relative; left:5%; font-family: STKaiti,Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,微软雅黑,Arial,sans-serif;">{{doc.children[0].label}}</p>
                                </el-collapse-item>
                            </el-collapse>
                        </el-collapse-item>
                    </el-card>
                </el-collapse>
            </div>
        </div>
</template>

<script>
    import {
        fetch
    } from '@/utils/communication'
    import API from "@/utils/API"
    import Cookies from "@/utils/cookies"

    export default {
        name: 'History',
        data() {
            return {
                data: [],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                }
            };
        },
        methods: {
            historyResponse(response) {
                console.log("文档返回内容", response)
                if (response.status == 200) {
                    console.log("history success: ", JSON.parse(response.data.data).data)
                    this.data = JSON.parse(response.data.data).data
                    this.HistoryIsEmpty = false
                    this.$forceUpdate()
                } else {
                    //this.$message.error("获取历史记录失败。请刷新重试。");
                    console.log("failed", response.data.data)
                    this.data = []
                    this.HistoryIsEmpty = true
                }
            },
            historyError(err) {
                console.log("err = " + err)
                this.$message.error('服务器连接异常，请检查网络:' + err)
                this.data = []
                this.HistoryIsEmpty = true
            },
            clearHistory() {
                this.$confirm('此操作将永久清空当前历史记录, 是否继续?', '警告', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let get_certificate = {
                        username: Cookies.getCookie("username"),
                        user_id: Cookies.getCookie("user_id"),
                        ask: "clearHistory",
                    }
                    fetch(API.GET_HISTORY.path, get_certificate, "请稍后...").then(response => {
                        this.historyResponse(response)
                    }).catch(err => {
                        this.historyError(err)
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消清空历史记录'
                    });
                })
            },
        },
        created() {
            let get_certificate = {
                username: Cookies.getCookie("username"),
                user_id: Cookies.getCookie("user_id"),
                ask: "history",
            }
            console.log(get_certificate)
            fetch(API.GET_HISTORY.path, get_certificate, "加载中，请稍后...").then(response => {
                this.historyResponse(response)
            }).catch(err => {
                this.historyError(err)
            })
        }
    };
</script>

<style scoped>
    .el-button {
        /*position: absolute;*/
        position: relative;
        float: inline-end;
        margin-right: 40px;
    }
    
    .el-card.question-card {
        width: 80%;
        left: 10%;
        position: relative;
        margin-bottom: 20px;
    }
    
    div.historyClearWrapper {
        white-space: normal;
        margin: 20px;
        /* align-content: flex-end; */
        width: 99%;
        height: 40px;
    }
    
    p.question {
        color: black;
    }
    
    p.question:hover {
        color: #409EFF;
    }
    
    p.doc {
        color: black;
    }
    
    p.doc:hover {
        color: #409EFF;
    }
</style>