import { mount, createLocalVue } from '@vue/test-utils'
import Home from '@/pages/Home.vue'
import Bus from '@/utils/bus'

const localVue = createLocalVue()
Bus(localVue)

describe('Home.vue', () => {
    const wrapper = mount(Home, { localVue })
    it('has a div', () => {
        const div = wrapper.find('div')
        expect(div.exists()).toBe(true)
    })
    it('test searchQuery function', () => {
        wrapper.vm.searchQuery("searchQuery")
    })
})