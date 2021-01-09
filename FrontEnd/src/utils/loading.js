import { Loading } from 'element-ui'

let loadingCount = 0
let loading

const startLoading = (show_text) => {
    console.log("测试缓冲：",show_text)
    loading = Loading.service({
        lock: true,
        //text: "搜肠刮肚思考回答中...",
        text: show_text,
        background: 'rgb(0,0,0,0.2)'
    })
}

const endLoading = () => {
    loading.close();
}

export const showLoading = (show_text) => {
    if (loadingCount === 0) {
        startLoading(show_text);
    }
    loadingCount += 1
}

export const hideLoading = () => {
    if (loadingCount <= 0) {
        return
    }
    loadingCount -= 1
    if (loadingCount === 0) {
        endLoading();
    }
}