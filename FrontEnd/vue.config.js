//const proxy = require('http-proxy-middleware');

module.exports = {
    devServer: {
        disableHostCheck: true,
        proxy: {
            '/docs': {
                target: 'https://db-demo-codedance.app.secoder.net', // Django服务器地址
                // target: 'http://183.173.148.126:8000',
                // target: 'http://183.173.146.183:8000',
                changOrigin: true,
            },
            '/user': {
                target: 'https://db-demo-codedance.app.secoder.net', // Django服务器地址
                // target: 'http://183.173.148.126:8000',
                // target: 'http://183.173.146.46:8000',
                changOrigin: true,
            },
        }
    }
}