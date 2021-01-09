/**
 * 如果需要修改为正常上线模式，请注释下面mock的import代码
 * **/
import axios from 'axios'
import { showLoading, hideLoading } from '@/utils/loading'

// 请在下方实现自己的后端通信函数
axios.defaults.withCredentials = true; //让ajax携带cookie
axios.defaults.timeout = 6000;

//请求拦截器即异常处理
axios.interceptors.request.use(request => {
        return request
    },
    err => {
        return Promise.reject(err);
    }
);

//响应拦截器即异常处理
axios.interceptors.response.use(response => {
    hideLoading();
    return response
}, err => {
    hideLoading();
    if (err && err.response) {
        console.log(`连接错误${err.response.status}`)
            /*switch (err.response.status) {
                case 400:
                    console.log('错误请求' + err.response.data.data)
                    break;
                case 401:
                    console.log('未授权，请重新登录')
                    break;
                case 403:
                    console.log('拒绝访问')
                    break;
                case 404:
                    console.log('请求错误,未找到该资源')
                    break;
                case 405:
                    console.log('请求方法未允许' + err.response.data.data)
                    break;
                case 408:
                    console.log('请求超时')
                    break;
                case 500:
                    console.log('服务器端出错')
                    break;
                case 501:
                    console.log('网络未实现')
                    break;
                case 502:
                    console.log('网络错误')
                    break;
                case 503:
                    console.log('服务不可用')
                    break;
                case 504:
                    console.log('网络超时')
                    break;
                case 505:
                    console.log('http版本不支持该请求')
                    break;
                default:
                    console.log(`连接错误${err.response.status}`)
            }*/
    } else {
        console.log('未知错误')
    }
    return Promise.resolve(err.response)
})

export function fetch(url, param, show_text, cookie = { withCredentials: true }) {
    console.log("cookies = " + "\"will give the cookie\"")
    console.log("cookies = " + cookie)
    console.log("cookies = " + "\"end of giving the cookie\"")
    console.log("parameters.ask = " + param.ask)
        //showLoading("搜肠刮肚思考回答中...")
    showLoading(show_text)
    return new Promise((resolve, reject) => {
        axios.get(url, {
                params: {
                    ask: param.ask,
                    username: param.username,
                    user_id: param.user_id
                }
            }, cookie)
            .then(response => {
                resolve(response);
            })
            .catch(err => {
                console.log("err() in get")
                reject(err)
            })
    })
}

export function post(url, data = {}, cookie = { withCredentials: true }) {
    showLoading("请稍后...");
    return new Promise((resolve, reject) => {
        axios.post(url, data, cookie)
            .then(response => {
                resolve(response);
            }, err => {
                console.log("err() in post")
                reject(err)
            })
    })
}