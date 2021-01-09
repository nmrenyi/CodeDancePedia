import { mount, createLocalVue } from '@vue/test-utils'
import NavBar from '@/components/NavBar.vue'
import Signin from '@/pages/Signin.vue'
import Signup from '@/pages/Signup.vue'
import VueRouter from "vue-router"
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)

describe('SearchBar.vue', () => {

    const router = new VueRouter({
        routes: [{
                path: '/sign_in',
                name: 'sign in',
                component: Signin
            },
            {
                path: '/sign_up',
                name: 'sign up',
                component: Signup
            }
        ]
    })

    const wrapper = mount(NavBar, { localVue, router })
    it('renders the correct markup', () => {
        expect(wrapper.html()).toContain('<div id="menuBar" class="menuBar">')
    })

    it('function test', () => {
        wrapper.vm.home()
            //wrapper.vm.$created()
        wrapper.vm.sign_in()
        wrapper.vm.sign_up()
        wrapper.vm.logout()
        wrapper.vm.user()
        wrapper.vm.history()
    })
})