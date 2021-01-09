import { mount } from '@vue/test-utils'
import SearchBar from '@/components/SearchBar.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()

describe('SearchBar.vue', () => {
  const wrapper = mount(SearchBar)
  it('has a form', () => {
    const form = wrapper.find('form')
    expect(form.exists()).toBe(true)
  })
  it('has a button', () => {
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
  })

  it('functions test', () => {
    const search_wrapper = shallowMount(SearchBar, {
      localVue,
      router
    })
    search_wrapper.vm.SearchQuery()
  })
})
