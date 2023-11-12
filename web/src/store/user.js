import userApi from "@/api/user";

export default {
    namespaced: true,
    state: {
        token: localStorage.getItem('token') || '',
        permUpdateTS: localStorage.getItem('permUpdateTS') || '',
        menus: JSON.parse(localStorage.getItem('menus')) || [],
        userData: JSON.parse(localStorage.getItem('userData')) || {},
        permissions: JSON.parse(localStorage.getItem('permissions')) || {},
    },
    getters: {
    },
    actions: {
        refreshPermissions(context) {
            userApi.getUserPersonal().then(({ data }) => {
                let { menus, user_data, permissions } = { ...data };
                context.commit("setMenus", menus);
                context.commit("setUserData", user_data);
                context.commit("setPermissions", permissions);
            });
        },
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
        setPermUpdateTS(state, permUpdateTS) {
            state.permUpdateTS = permUpdateTS;
            localStorage.setItem('permUpdateTS', permUpdateTS)
        },
        clearAll(state) {
            state.token = '';
            state.menus = [];
            state.userData = {};
            state.permissions = [];
            localStorage.removeItem('token')
            localStorage.removeItem('menus')
            localStorage.removeItem('userData')
            localStorage.removeItem('permissions')
            localStorage.removeItem('permUpdateTS')
        }
    }
}


