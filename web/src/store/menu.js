export default {
    namespaced: true,
    state: {
        routers: JSON.parse(localStorage.getItem('routers')) || [],
        isCollapse: false,  // 侧边栏是否缩起
        menuHistroy: [],
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
        // 菜单历史数据
        updateMenuHistroy(state, new_route) {
            if (new_route.name === 'login' || new_route.name === 'main') return
            let r = state.menuHistroy.find((x) => {
                return x.name == new_route.name
            })
            if (r) return;
            let getTitle = () => {
                for (const i of state.routers) {
                    let t = i.children.find((x) => {
                        return x.name == new_route.name
                    })
                    if (t) return t.meta.title
                }
            }
            let title = getTitle();
            if (! title) return
            let router = { 'name': new_route.name, 'title': getTitle()};
            state.menuHistroy.push(router)
            if (state.menuHistroy.length > 10) {
                state.menuHistroy.splice(0, 1);
            }
        },
        deleteMenuHistory(state, route) {
            let index = state.menuHistroy.findIndex((x) => {
                return x.name == route.name
            })
            if (index === -1) return
            state.menuHistroy.splice(index, 1)
        }
    }
}


