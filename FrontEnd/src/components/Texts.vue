<template>
    <div style="position: relative;">
        <el-collapse style="align-content: center; border-color: rgba(0, 0, 0, 0)" v-model="activeNames" @change="handleChange">
            <div v-bind:key="text.id" v-for="text in texts">
                <el-card class="text_item">
                    <TextItem v-bind:text="text"/>
                </el-card>
            </div>
        </el-collapse>
        <div style="height: 250px; width: 100%; position: relative;"></div>
    </div>
</template>

<script>
    import TextItem from './TextItem.vue'

    export default {
        name: "Texts",
        components: {
            TextItem
        },
        props: ["texts"],
        data() {
            return {
                activeNames: [1]
            }
        }
    }
</script>

<style scoped>
    div.text_item {
        width: 70%;
        position: relative;
        left: 15%;
        margin: 20px;
        opacity: 0.6;
    }
    
    div.text_item:hover {
        opacity: 0.9;
        width: 72%;
        left: 14%;
    }
</style>