export default {
    namespaced: true,
    state: {
        routers: JSON.parse(localStorage.getItem('routers')) || [],
        isCollapse: false,  // 侧边栏是否缩起
    },
    getters: {
        collapse(state){
            return state.isCollapse
        },
        sidebarWidth(state) {
            return state.isCollapse ? '60px' : "200px";
        }
    },
    mutations: {
        // 更新侧边栏伸缩状态
        updateCollapse(state) {
            state.isCollapse = !state.isCollapse;
        },
        // 更新前端路由
        updateRouters(state, routers) {
            state.routers = routers;
            localStorage.setItem('routers', JSON.stringify(routers))
        },
    }
}


