export default {
    namespaced: true,
    state: {
        token: localStorage.getItem('token') || '',
        menus: JSON.parse(localStorage.getItem('menus')) || [],
        userData: JSON.parse(localStorage.getItem('userData')) || {},
        permissions: JSON.parse(localStorage.getItem('permissions')) || {},
    },
    getters: {
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
            localStorage.setItem('token', token)
        },
        setUserData(state, userData) {
            state.userData = userData;
            localStorage.setItem('userData', JSON.stringify(userData))
        },
        setMenus(state, menus) {
            state.menus = menus;
            localStorage.setItem('menus', JSON.stringify(menus))
        },
        setPermissions(state, permissions) {
            state.permissions = permissions;
            localStorage.setItem('permissions', JSON.stringify(permissions))
        },
        clearAll() {
            state.token = [];
            state.menus = [];
            state.userData = [];
            state.permissions = [];
            localStorage.removeItem('token')
            localStorage.removeItem('menus')
            localStorage.removeItem('userData')
            localStorage.removeItem('permissions')
        }
    }
}


