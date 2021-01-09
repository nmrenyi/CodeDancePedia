const API = {
    GET_ASK_FOR_ANSWER: {
        path: "/docs/search",
        method: "get"
    },
    POST_USER_SIGNUP: {
        path: "/user/register/",
        method: "post"
    },
    POST_USER_SIGNIN: {
        path: "/user/login/",
        method: "post"
    },
    POST_USER_INFO: {
        path: "/user/info",
    },
    GET_HISTORY: {
        path: "/user/history/",
        method: "get"
    },
    POST_DOC_MODIFY: {
        path: "/docs/modify/",
        method: "post"
    },
    POST_DOC_UPLOAD: {
        path: "/docs/upload/",
        method: "post"
    }
}

export default API