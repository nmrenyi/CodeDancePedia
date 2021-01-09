import UserInfo from '@/components/UserInfo.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import { Form, Input, Button } from 'element-ui'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

var JsonStr = '{"uername": "文本正文", "user_id":"标题","bios":"个人简介"} '


describe('Modify_Doc.vue', () => {
    const wrapper = shallowMount(UserInfo, {
        localVue,
        router
    })

    it('has a form', () => {
        const input = wrapper.findComponent(Form)
        expect(input.exists()).toBe(true)
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
        wrapper.vm.$mount()
        wrapper.vm.onSubmit()
        wrapper.vm.reset()
    })

    it('submit success, status == 200', () => {
        wrapper.vm.submitResponse({
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
                "data": "Bad Request"
            }
        })
    })

    /*
    it('confirm success, status == 201', () => {
        wrapper.vm.confirmResponse({
            status: 201,
            data: {
                "data": "Bad Request"
            }
        })
    })
    it('delete success, status == 201', () => {
        wrapper.vm.deleteResponse({
            status: 201,
            data: {
                "data": "Bad Request"
            }
        })
    })
    */
})