import User from '@/pages/User.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

describe('User.vue', () => {
    const wrapper = shallowMount(User, {
        localVue,
        router
    })
    it('has a div', () => {
        const div = wrapper.find('div')
        expect(div.exists()).toBe(true)
    })

    it('functions test', () => {
        wrapper.vm.$mount()
        wrapper.vm.user_change({
            username: "username",
            user_id: "user_id",
            bio: "bio",
            password: "password"
        })
        wrapper.vm.label_change("用户管理")
    })
})