import { mount } from '@vue/test-utils'
import signup from '@/pages/Signup.vue'
import { createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import Axios from 'axios'

var JsonStr = '{"username": "文本正文", "user_id":"标题"} '

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

jest.mock('axios')
describe('Signup.vue', () => {
    const wrapper = mount(signup, { localVue, router })

    it('axios test signup', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.signup()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.signup()
        expect(data_received2).toBe(undefined)
    })
})