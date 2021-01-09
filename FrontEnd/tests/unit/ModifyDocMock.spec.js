import Modify_Doc from '@/components/Modify_Doc.vue'
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
describe('Modify_Doc.vue axios', () => {
    const wrapper = shallowMount(Modify_Doc, {
        localVue,
        router
    })

    it('axios test submitSearch', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.submitSearch()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.submitSearch()
        expect(data_received2).toBe(undefined)
    })

    it('axios test confirm', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.confirm()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.confirm()
        expect(data_received2).toBe(undefined)
    })

    it('axios test del', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.del()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.del()
        expect(data_received2).toBe(undefined)
    })

    it('axios test restore', async() => {
        Axios.post.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.restore()
        expect(data_received1).toBe(undefined)

        Axios.post.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.restore()
        expect(data_received2).toBe(undefined)
    })

})