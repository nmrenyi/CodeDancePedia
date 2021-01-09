import { mount, createLocalVue } from '@vue/test-utils'
//import axios from 'axios'
import QueryResult from '@/pages/QueryResult.vue'
import VueRouter from "vue-router"
import navBar from '@/components/NavBar.vue'
import searchBar from '@/components/SearchBar.vue'
import Texts from '@/components/Texts.vue'
import ElementUI from 'element-ui'

var TestTexts_credit = [{
    id: 1,
    answer: "Texts:1",
    grade: 65.4,
    credit: 1,
    content: "ContentContentContentTexts:1,ContentContent",
}, {
    id: 2,
    answer: "Texts:2",
    grade: 55.4,
    credit: 1,
    content: "ContentContentContentTexts:2,ContentContent",
}, {
    id: 3,
    answer: "Texts:3",
    grade: 45.4,
    credit: 0,
    content: "ContentContentContentTexts:3,ContentContent",
    completed: false
}]

var TestTexts_no_credit = [{
    id: 1,
    answer: "Texts:3",
    grade: 35.4,
    credit: 0,
    content: "ContentContentContentTexts:3,ContentContent",
    completed: false
}, {
    id: 2,
    answer: "Texts:6",
    grade: 19.4,
    credit: 0,
    content: "ContentContentContentTexts:6,ContentContent",
    completed: false
}]


const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(navBar)
localVue.use(searchBar)
localVue.use(Texts)
localVue.use(ElementUI)

//axios.defaults.withCredentials = true; //让ajax携带cookie
//localVue.prototype.$axios = axios;

localVue.filter('highlight', function(word, query) {
    var check = new RegExp(query, "ig");
    return word.toString().replace(check, function(matchedText) {
        return ('<span style="color:blue;font-weight:bold">' + matchedText + '</span>');
    });
});

describe('QueryResult.vue', () => {
    const router = new VueRouter({
        routes: [{
            path: '/query_result',
            name: 'query result',
            component: QueryResult
        }]
    })
    router.push({
        path: '/query_result',
        query: {
            search_content: "test search"
        }
    });

    const wrapper = mount(QueryResult, { localVue, router })
    it('has a navBar', () => {
        expect(wrapper.findComponent(navBar).exists()).toBe(true)
    })
    it('has a searchBar', () => {
        expect(wrapper.findComponent(searchBar).exists()).toBe(true)
    })
    it('has a Texts', () => {
        expect(wrapper.findComponent(Texts).exists()).toBe(true)
    })

    /*
    it('get texts and show', () => {
        const vm = wrapper.vm
            // test the added data
        vm.searchQuery()
        localVue.nextTick(() => {
            localVue.nextTick(() => {
                expect(vm.texts).toEqual(TestTexts)
            })
        })
    })*/


    it('has div inside', () => {
        const div = wrapper.findAll("div")
        expect(div.exists()).toBe(true)
    })

    it('functions test', () => {
        wrapper.vm.$mount()
        wrapper.vm.searchQuery("query")
        wrapper.vm.closeDialog()
        wrapper.vm.QueryError()
    })

    it('response test, status == 200, with credit', () => {
        wrapper.vm.QueryResponse({
            "status": 200,
            "time": 365,
            "data": {
                "data": TestTexts_credit
            }
        })
    })

    it('response test, status == 200, without credit', () => {
        wrapper.vm.QueryResponse({
            "status": 200,
            "time": 365,
            "data": {
                "data": TestTexts_no_credit
            }
        })
    })

    it('response test, status == 500', () => {
        wrapper.vm.QueryResponse({
            "status": 500,
            "data": {
                "data": TestTexts_credit
            }
        })
    })

    it('response test, status == 204', () => {
        wrapper.vm.QueryResponse({
            "status": 204,
            "data": {
                "data": TestTexts_credit
            }
        })
    })

    it('response test, status == 400', () => {
        wrapper.vm.QueryResponse({
            "status": 400,
            "data": {
                "data": TestTexts_credit
            }
        })
    })


})