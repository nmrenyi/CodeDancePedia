import { mount, createLocalVue } from '@vue/test-utils'
import History from '@/components/History.vue'
import ElementUI, { Button, Collapse } from 'element-ui'

//jest.mock("@/utils/communication")
const localVue = createLocalVue()
localVue.use(ElementUI)

var JsonStr = '{"data": "[{label: \'一\',children: [{label: \'二\',children: [{label: \'三\'}]}]}]" }'

describe('History.vue', () => {
    const wrapper = mount(History, { localVue })
    it('has div inside', () => {
        const div = wrapper.findAll("div")
        expect(div.exists()).toBe(true)
    })

    it('has an el-button and Collapse', () => {
        expect(wrapper.findComponent(Button).exists()).toBe(true);
        expect(wrapper.findComponent(Collapse).exists()).toBe(true);
    })

    it('no-axios test', () => {
        wrapper.vm.$createElement()
        wrapper.vm.clearHistory()
    })

    it('test historyResponse, status==200', () => {
        wrapper.vm.historyResponse({
            status: 200,
            data: {
                "data": JsonStr
            }
        })
    })
    it('test historyResponse, status==500', () => {
        wrapper.vm.historyResponse({
            status: 500,
            data: {
                "data": JsonStr
            }
        })
    })
    it('test historyError', () => {
        wrapper.vm.historyError({
            err: "Error"
        })
    })
})