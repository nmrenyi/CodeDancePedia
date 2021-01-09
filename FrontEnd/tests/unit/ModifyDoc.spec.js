import Modify_Doc from '@/components/Modify_Doc.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import { Input, Button } from 'element-ui'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

var JsonStr = '{"content": "文本正文", "title":"标题","code": "7", "detail":"报错信息"} '


describe('Modify_Doc.vue', () => {
    const wrapper = shallowMount(Modify_Doc, {
        localVue,
        router
    })
    it('has a input', () => {
        const input = wrapper.findComponent(Input)
        expect(input.exists()).toBe(true)
    })

    it('has a button', () => {
        const button = wrapper.findComponent(Button)
        expect(button.exists()).toBe(true)
    })

    it('functions test', () => {
        wrapper.vm.submitSearch()
        wrapper.vm.editChanged()
        wrapper.vm.cancel()
        wrapper.vm.confirm()
        wrapper.vm.del()
        wrapper.vm.restore()
    })

    it('submit success, status == 200', () => {
        wrapper.vm.submitResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })
    it('confirm success, status == 200', () => {
        wrapper.vm.confirmResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })
    it('delete success, status == 200', () => {
        wrapper.vm.deleteResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })
    it('restore success, status == 200', () => {
        wrapper.vm.restoreResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })
    it('submit error, status == 201', () => {
        wrapper.vm.submitResponse({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
    })
    it('confirm error, status == 201', () => {
        wrapper.vm.confirmResponse({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
    })
    it('delete error, status == 201', () => {
        wrapper.vm.deleteResponse({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
    })
    it('restore error, status == 201', () => {
        wrapper.vm.restoreResponse({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
    })
})