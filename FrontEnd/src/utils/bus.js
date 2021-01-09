export default (Vue) => {
    const eventBus = new Vue()
    Vue.prototype.$bus = {
        $on(...param) {
            eventBus.$on(...param)
        },
        $off(...param) {
            eventBus.$off(...param)
        },
        $once(...param) {
            eventBus.$once(...param)
        },
        $emit(...param) {
            eventBus.$emit(...param)
        }
    }
}