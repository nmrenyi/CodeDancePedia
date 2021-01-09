<template>
    <el-container class="uploadContainer">
        <el-aside width = "35%" height="100%" class="uploadedFilesDisplay">
            <el-card style="height:99%" class="uploadedDocListContianer">
                <p class="uploadedDocList">本次已上传文件列表</p>
                <el-tag
                class="elementUI-tag"
                v-for="filee in uploadFileList"
                :key="filee.name"
                type="info"
                effect="plain">
                {{filee.name}}
                </el-tag>
            </el-card>
            <!--<div class="verticalBar"></div>-->
            <!--<el-divider direction="vertical"></el-divider>-->
        </el-aside>
        <el-container class="mainUpload">
            <el-main>
                <el-upload
                    class="uploadFiles"
                    ref="upload"
                    :action="url"
                    :on-remove="handleRemove"
                    :auto-upload="false"
                    :before-upload="handleBeforeUpload"
                    :on-success="handleSuccess"
                    :on-error="handleError"   
                    multiple
                    :with-credentials="true"
                    drag
                    :show-file-list="showSubmittedFile">
                    <!--:file-list="fileList"-->

                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <!--<el-button slot="trigger" size="small" type="primary">选取文件</el-button>-->
                    <div slot="tip" class="el-upload__tip">只能上传json文件，且单个文件大小不超过2Mb</div>
                    <div slot="tip" class="el-upload__tip">一个json文件可以含有多篇文档, 文件结构应类似于</div>
                    <div slot="tip" class="el-upload__tip">{"data":[{"paragraphs":[{"context":正文,"title":标题},{"context":正文,"title":标题}]}]}</div>
                </el-upload>
                <div>
                    <p class="href"><a href="https://cloud.tsinghua.edu.cn/f/0733f86261b246aba1ab/?dl=1">下载上传json文件的模板</a></p>
                    <el-button style="margin-top: 10px; align-self: center;" size="small" type="success" @click="submitUpload">上传到数据库</el-button>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
    //import { post } from '@/utils/communication'
    import API from "@/utils/API"
    //import Cookies from "@/utils/cookies"

    var isJSON;
    var fileSize;
    //var currentUploadList;

    export default {
        name: "Upload_Doc",
        data() {
            return {
                fileList: [],
                uploadFileList: [],
                uploadBuffer: Object(),
                showSubmittedFile: true,
                url: API.POST_DOC_UPLOAD.path
            }
        },
        methods: {
            mounted() {
                fileSize = 0
                    //currentUploadList = []
            },
            submitUpload() {
                console.log("in submitUpload method")
                this.$refs.upload.submit();
                console.log("submit done")
                fileSize = 0
            },
            handleBeforeUpload(file) {
                console.log(file)
                isJSON = (file.type === 'application/json')
                fileSize = file.size / 1024 / 1024;
                var flag = true
                if (!isJSON) {
                    this.$message.error('上传的必须是json格式的文件！(出错文件：' + file.name + ')')
                    flag = false
                }
                if (fileSize >= 2) {
                    this.$message.error('上传文件大小不能超过2MB!(出错文件：' + file.name + ')')
                    flag = false
                }
                this.$forceUpdate()
                return flag
            },
            handleSuccess(response, file, filelist) {
                console.log("hadleSuccess")
                console.log("upload Buffer", this.uploadBuffer)
                console.log("success list", response, file, filelist)
                for (var ff of filelist) {
                    console.log(ff.name + " " + JSON.parse(ff.response.data).document_id)
                    var data = JSON.parse(ff.response.data)
                    this.uploadBuffer[data.document_id] = {
                        name: ff.name + "  id:" + data.document_id
                    }
                }
                this.SyncUploadFiles()
                    //this.$message.success('上传成功')
                this.fileList = []
                this.$refs.upload.clearFiles()
                this.$forceUpdate()
            },
            handleError(response, file) {
                if (response["status"] == 400)
                    this.$message.error('用户身份验证失败，仅管理员可以使用此功能~ (出错文件：' + file.name + ')')
                else if (response["status"] == 401)
                    this.$message.error('上传文档格式错误~ (出错文件：' + file.name + ')')
                else if (response["status"] == 402)
                    this.$message.error('上传文档中缺乏title或者context字段~ (出错文件：' + file.name + ')')
                else if (response["status"] == 403)
                    this.$message.error('上传文档验证失败~ (出错文件：' + file.name + ')')
                else if (response["status"] == 405)
                    this.$message.error('Cookie缺乏字段~ (出错文件：' + file.name + ')')
                else if (response["status"] == 406)
                    this.$message.error('上传文档Json解码失败~ (出错文件：' + file.name + ')')
                else if (response["status"] == 407)
                    this.$message.error('上传文档编码方式不支持，请使用utf-8编码方式~ (出错文件：' + file.name + ')')
                else
                    this.$message.error('上传文档失败~ (出错文件：' + file.name + ')')
            },
            SyncUploadFiles() {
                this.uploadFileList = []
                for (var id in this.uploadBuffer) {
                    this.uploadFileList.push(this.uploadBuffer[id])
                }
            }
        },
    }
</script>

<style scoped>
    .verticalBar {
        display: inline-block;
        width: 1px;
        height: 100%;
        margin: 0 8px;
        vertical-align: middle;
        position: relative;
        color: gray;
    }
    
    p.uploadedDocList {
        margin-bottom: 10px;
    }
    
    .elementUI-tag {
        margin: 3px;
    }
    
    .mainUpload {
        align-content: center;
    }
    
    .href {
        margin-top: 2px;
        margin-bottom: 5px;
        color: #707070;
        font-size: 13px;
    }
    
    a:visited {
        color: #909090;
    }
    
    a:hover {
        color: #909090;
    }
    
    a:link {
        color: #909090;
    }
    
    a:active {
        color: #909090;
    }
</style>