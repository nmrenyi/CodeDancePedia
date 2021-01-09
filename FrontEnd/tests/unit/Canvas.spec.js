import { mount, createLocalVue } from '@vue/test-utils'
import Canvas from '@/components/Canvas.vue'
import * as THREE from 'three'

const localVue = createLocalVue()
localVue.use(THREE)

describe('Canvas.vue', () => {
    const wrapper = mount(Canvas, { localVue })
    it('has div inside', () => {
        const div = wrapper.findAll("div")
        expect(div.exists()).toBe(true)
    })
})