// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import Home from '@/pages/Home.vue'
import About from '@/pages/About.vue'
import Signin from '@/pages/Signin.vue'
import Signup from '@/pages/Signup.vue'
import User from '@/pages/User.vue'
import QueryResult from '@/pages/QueryResult.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueCookie from 'vue-cookies'
import axios from 'axios'
import Bus from '@/utils/bus.js'

/* eslint-disable no-new */
Vue.use(Router)
const originalReplace = Router.prototype.replace;
Router.prototype.replace = function replace(location) {
    return originalReplace.call(this, location).catch(err => err);
};
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

const router = new Router({
    routes: [{
            path: '/',
            name: 'home',
            meta: { index: 0 },
            component: Home
        },
        {
            path: '/sign_in',
            name: 'sign in',
            component: Signin
        },
        {
            path: '/sign_up',
            name: 'sign up',
            component: Signup
        },
        {
            path: '/query_result',
            name: 'query result',
            meta: { index: 1 },
            component: QueryResult
        },
        {
            path: '/user',
            name: 'user',
            component: User
        },
        {
            path: '/about',
            name: 'about',
            component: About
        },
    ]
})


Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.use(VueCookie)

axios.defaults.withCredentials = true; //让ajax携带cookie
Vue.prototype.$axios = axios;

Bus(Vue)

Vue.filter('highlight', function(word, query) {
    //eslint-disable-next-line
    var parentheses = new RegExp(/[\(\)\[\]\{\}\?\*\+\.\&\^]/, "img");
    query = query.toString().replace(parentheses, function(matchParentheses) {
        return ('[' + matchParentheses + ']')
    })
    var check = new RegExp(query, "img")
    return word.toString().replace(check, function(matchedText) {
        return ('<span style="color:blue;font-weight:bold">' + matchedText + '</span>');
    });
});

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')