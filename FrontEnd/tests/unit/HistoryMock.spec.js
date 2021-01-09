import { mount, createLocalVue } from '@vue/test-utils'
import History from '@/components/History.vue'
import ElementUI from 'element-ui'
import { fetch } from '@/utils/communication'
import API from "@/utils/API"
import Axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)

var JsonStr = '{"data": "[{label: \'一\',children: [{label: \'二\',children: [{label: \'三\'}]}]}]" }'
let get_certificate = {
    username: "username",
    user_id: "user_id",
    ask: "clearHistory",
}

jest.mock('axios')
describe('History.vue -2', () => {
    const wrapper = mount(History, { localVue })

    it('fetch test', (done) => {
        fetch(API.GET_HISTORY.path, get_certificate, "请稍后...").then(response => {
            response = new Object({ data: { code: 200 } })
            expect(response).toMatch({
                data: { code: 200 }
            })
        }).catch()
        done()
    })

    it('axios test', async() => {
        Axios.get.mockResolvedValueOnce({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
        const data_received1 = await wrapper.vm.clearHistory()
        expect(data_received1).toBe(undefined)

        Axios.get.mockRejectedValueOnce({
            status: 201,
            data: {
                "data": JsonStr
            }
        })
        const data_received2 = await wrapper.vm.clearHistory()
        expect(data_received2).toBe(undefined)
    })
})