import signin from '@/pages/Signin.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import Axios from 'axios'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()
localVue.use(ElementUI)

var JsonStr = '{"username": "文本正文", "user_id":"标题"} '

jest.mock('axios')
describe('Signin.vue', () => {
    const wrapper = shallowMount(signin, { localVue, router })
    it('axios test signin', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.signin()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.signin()
        expect(data_received2).toBe(undefined)
    })

})