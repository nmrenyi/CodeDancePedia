import User from '@/pages/User.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import Axios from 'axios'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(ElementUI)
const router = new VueRouter()

var JsonStr = '{"content": "文本正文", "title":"标题","code": "7", "detail":"报错信息"} '


jest.mock('axios')
describe('User.vue', () => {
    const wrapper = shallowMount(User, {
        localVue,
        router
    })

    it('axios test $mount', async() => {
        Axios.get.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1_200 = await wrapper.vm.mountFunction()
        expect(data_received1_200).toBe(undefined)

        Axios.get.mockResolvedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received1_201 = await wrapper.vm.mountFunction()
        expect(data_received1_201).toBe(undefined)

        Axios.get.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.mountFunction()
        expect(data_received2).toBe(undefined)

        wrapper.vm.$mount()
    })
})