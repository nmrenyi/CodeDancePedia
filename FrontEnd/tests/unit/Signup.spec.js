import { mount } from '@vue/test-utils'
import signup from '@/pages/Signup.vue'
import { createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI, { Form, Button, Input } from 'element-ui'

var JsonStr = '{"username": "文本正文", "user_id":"标题"} '

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

describe('Signup.vue', () => {
    const wrapper = mount(signup, { localVue, router })

    // components
    it('has a form', () => {
        const form = wrapper.findComponent(Form)
        expect(form.exists()).toBe(true)
    })
    it('has a button', () => {
        const button_group = wrapper.findAllComponents(Button)
        expect(button_group.at(0).classes()).toContain('cancel')
        expect(button_group.at(1).classes()).toContain('register')
    })
    it('has a input', () => {
        const input = wrapper.findComponent(Input)
        expect(input.exists()).toBe(true)
    })
    it('has a input', () => {
        const input = wrapper.find(Input)
        input.element.data = "abc"
        input.trigger("change")
        expect(input.exists()).toBe(true)
    })

    //functions
    it('functions test', () => {
        wrapper.vm.signup()
        wrapper.vm.cancel()
        wrapper.vm.closeDialog()
    })

    it('signup response, status == 200', () => {
        wrapper.vm.signupResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })

    it('signup response, status != 200', () => {
        wrapper.vm.signupResponse({
            status: 400,
            data: {
                "data": JsonStr
            }
        })
    })
})