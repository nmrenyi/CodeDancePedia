import { mount, createLocalVue } from '@vue/test-utils'
//import axios from 'axios'
import QueryResult from '@/pages/QueryResult.vue'
import VueRouter from "vue-router"
import navBar from '@/components/NavBar.vue'
import searchBar from '@/components/SearchBar.vue'
import Texts from '@/components/Texts.vue'
import ElementUI from 'element-ui'
import Axios from 'axios'

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

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(navBar)
localVue.use(searchBar)
localVue.use(Texts)
localVue.use(ElementUI)

localVue.filter('highlight', function(word, query) {
    var check = new RegExp(query, "ig");
    return word.toString().replace(check, function(matchedText) {
        return ('<span style="color:blue;font-weight:bold">' + matchedText + '</span>');
    });
});

jest.mock('axios')
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

    it('function searchQuery test', async() => {
        Axios.get.mockResolvedValueOnce({
            "status": 200,
            "time": 365,
            "data": {
                "data": TestTexts_credit
            }
        })
        const data_received1 = await wrapper.vm.searchQuery("query")
        expect(data_received1).toBe(undefined)

        Axios.get.mockRejectedValueOnce({
            "status": 201,
            "time": 365,
            "data": {
                "data": TestTexts_credit
            }
        })
        const data_received2 = await wrapper.vm.searchQuery("query")
        expect(data_received2).toBe(undefined)
    })
})