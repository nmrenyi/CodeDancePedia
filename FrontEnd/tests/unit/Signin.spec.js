import signin from '@/pages/Signin.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI, { Form, Button, Input } from 'element-ui'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()
localVue.use(ElementUI)

var JsonStr = '{"username": "文本正文", "user_id":"标题"} '

describe('Signin.vue', () => {
    const wrapper = shallowMount(signin, { localVue, router })
        // components
    it('has a form', () => {
        const form = wrapper.findComponent(Form)
        expect(form.exists()).toBe(true)
    })
    it('has a button', () => {
        const button_group = wrapper.findAllComponents(Button)
        expect(button_group.at(0).classes()).toContain('cancel')
        expect(button_group.at(1).classes()).toContain('confirm')
    })
    it('has a input', () => {
        const input = wrapper.findComponent(Input)
        expect(input.exists()).toBe(true)
    })

    //functions
    it('functions test', () => {
        wrapper.vm.signin()
        wrapper.vm.cancel()
        wrapper.vm.closeDialog()
    })

    it('signin response, status == 200', () => {
        wrapper.vm.signinResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })

    it('signin response, status != 200', () => {
        wrapper.vm.signinResponse({
            status: 400,
            data: {
                "data": JsonStr
            }
        })
    })
})