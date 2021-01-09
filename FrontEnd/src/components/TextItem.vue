<template>
    <div class='text-item' v-bind:class="{'is-complete':text.completed}">
        <el-collapse-item :name="text.id">
            <template slot="title">
                <div class="head_wrapper" id="head_wrapper" style="width: 98%;">
                    <p class="answer" align="left" style="float: left; overflow: hidden; text-overflow:ellipsis; white-space:nowrap;">{{text.answer}}</p>
                    <p align="right">{{text.grade}}</p>
                </div>
            </template>
<div class="content">
    <p class="content_doc_id">{{text.doc_id}}</p>
    <div class="content_head">
        <p class="title">{{text.title}}</p>
        <p class="source">来源：{{text.src}}</p>
    </div>
    <span v-html="$options.filters.highlight(text.content, text.answer)" class="content" id="content">{{text.content}}</span>
</div>
<div class="creditLevel" style="margin-top:25px;">
    <span class="content_credit_degree">答案可信度：</span>
    <span class="credit_level_2" v-if="text.credit == 2">
        <el-progress :text-inside="true" :stroke-width="20" :percentage="text.grade" status="success"></el-progress>
    </span>
    <span class="credit_level_1" v-else-if="text.credit == 1">
        <el-progress :text-inside="true" :stroke-width="20" :percentage="text.grade" status="warning"></el-progress>
    </span>
    <span class="credit_level_0" v-else>
        <el-progress :text-inside="true" :stroke-width="20" :percentage="text.grade" status="exception"></el-progress>
    </span>
    <span class="credit_space"></span>
</div>
</el-collapse-item>
</div>
</template>

<script>
    export default {
        name: "TextItem",
        props: ["text"],
        data() {
            return {
                activeNames: [1],
                comment_edit: "",
                comments: ["Alice: this is a good document!", "Bob: emmm, good!", "Carrot: I like this document!"]
            }
        }
    }
</script>

<style scoped>
    .text-item {
        /* background: #f4f4f4; */
        margin: 5px;
        padding: 5px;
        /* border-bottom: 1px #ccc dotted; */
        border-radius: 5px;
    }
    
    .is-complete {
        text-decoration: line-through;
    }
    
    div.el-collapse-item {
        background-color: #f4f4f4;
        /* border-bottom: 1px #ccc dotted; */
        border-radius: 5px;
    }
    
    div.creditLevel {
        white-space: nowrap;
        overflow-x: auto;
        width: 100%;
    }
    
    span.content_credit_degree {
        display: inline-block;
        width: 8%;
        text-align: left;
        padding-left: 5px;
    }
    
    span.credit_level_2 {
        display: inline-block;
        width: 50%;
        position: relative;
    }
    
    span.credit_level_1 {
        display: inline-block;
        width: 50%;
        position: relative;
    }
    
    span.credit_level_0 {
        display: inline-block;
        width: 50%;
        position: relative;
    }
    
    span.credit_space {
        display: inline-block;
        width: 40%;
    }
    
    div.el-collapse-item__header {
        background-color: #f4f4f4;
    }
    
    div.el-collapse-item__wrap {
        background-color: #f4f4f4;
    }
    
    p.answer {
        font-size: large;
        padding-left: 5px;
        margin-left: 5px;
        font-size: 21px;
    }
    
    p.content_doc_id {
        padding-bottom: 3px;
        color: #808080;
        font-size: 13px;
    }
    
    p.title {
        font-weight: bold;
        font-size: medium;
        display: inline-block;
        font-size: 18px;
    }
    
    p.source {
        color: #808080;
        margin-left: 10px;
        display: inline-block;
        font-size: 13px;
    }
    
    div.content_head {
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    div.content {
        margin-top: 10px;
        padding-left: 10px;
        padding-right: 10px;
        text-align: left;
        font-size: 15px;
    }
</style>