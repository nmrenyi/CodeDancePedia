import UserInfo from '@/components/UserInfo.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import Axios from 'axios'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

var JsonStr = '{"uername": "文本正文", "user_id":"标题","bios":"个人简介"} '


jest.mock('axios')
describe('Modify_Doc.vue', () => {
    const wrapper = shallowMount(UserInfo, {
        localVue,
        router
    })

    it('axios test onSubmit', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.onSubmit()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.onSubmit()
        expect(data_received2).toBe(undefined)
    })
})