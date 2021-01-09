import { mount, createLocalVue } from '@vue/test-utils'
import Upload_Doc from '@/components/Upload_Doc.vue'
import ElementUI from 'element-ui'
import { Upload } from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

var successResponse = { code: 200, data: "{\"document_id\": 3767}" }
var errorResponse = { code: 400, data: "{\"不是管理员\"}" }

var successFileList = [{
    name: "testfile.json",
    type: 'application/json',
    size: 1 * 1024 * 1024,
    response: successResponse
}, {
    name: "b.json",
    type: 'application/json',
    size: 1 * 1024 * 1024,
    response: successResponse
}, {
    name: "a.json",
    type: 'application/json',
    size: 1 * 1024 * 1024,
    response: successResponse
}]

describe('Upload_Doc.vue', () => {
    const wrapper = mount(Upload_Doc, { localVue })
    it('has div inside', () => {
        const div = wrapper.findAll("div")
        expect(div.exists()).toBe(true)
    })
    it('has an el-upload', () => {
        expect(wrapper.findComponent(Upload).exists()).toBe(true);
    })


    it('functions test', () => {
        wrapper.vm.$mount()
        wrapper.vm.submitUpload()
    })

    // test beforeUpload
    it('file beforeUpload test :: too large', () => {
        wrapper.vm.handleBeforeUpload({
            name: "testfile.json",
            type: 'application/json',
            size: 3 * 1024 * 1024
        })
    })
    it('file beforeUpload test :: not json', () => {
        wrapper.vm.handleBeforeUpload({
            name: "testfile.png",
            type: 'image/x-png',
            size: 1 * 1024 * 1024
        })
    })
    it('file beforeUpload test :: okay', () => {
        wrapper.vm.handleBeforeUpload({
            name: "testfile.json",
            type: 'application/json',
            size: 1 * 1024 * 1024
        })
    })

    //test handleSuccess
    it('function handleSuccess test', () => {
        wrapper.vm.handleSuccess(successResponse, {
            name: "testfile.json",
            type: 'application/json',
            size: 1 * 1024 * 1024
        }, successFileList)
    })

    it('function handleError test', () => {
        wrapper.vm.handleError(errorResponse, {
            name: "testfile.png",
            type: 'application/json',
            size: 1 * 1024 * 1024
        })
    })
})