import http from "@/http";

export default {

    // 登陆
    login: function (username, password) {
        return http.post('/oauth/login', { username, password })
    },

    // 获取全部用户
    getUsers: function () {
        return http.get('/oauth/user/', {})
    },

    // 获取全部用户
    getComboUsers: function () {
        return http.get('/oauth/user/combo_info/', {})
    },

    // 新增用户
    createUser: function (data) {
        return http.post('/oauth/user/', data)
    },

    // 更新用户
    updateUser: function (pk, data) {
        return http.put(`/oauth/user/${pk}/`, data)
    },

    // 删除用户
    deleteUser: function (pk) {
        return http.delete(`/oauth/user/${pk}/`)
    },

    // 获取权限
    getPermission: function () {
        return http.get('/oauth/permission/', {})
    },

    // 获取权限
    getComboPermissions: function () {
        return http.get('/oauth/permission/combo_info/', {})
    },

    // 新增权限
    createPermission: function (data) {
        return http.post('/oauth/permission/', data)
    },

    // 更新权限
    updatePermission: function (pk, data) {
        return http.put(`/oauth/permission/${pk}/`, data)
    },

    // 删除权限
    deletePermission: function (pk) {
        return http.delete(`/oauth/permission/${pk}/`)
    },

    // 获取菜单
    getMenu: function () {
        return http.get('/oauth/menu/', {})
    },

    // 新增菜单
    createMenu: function (data) {
        return http.post('/oauth/menu/', data)
    },

    // 更新菜单
    updateMenu: function (pk, data) {
        return http.put(`/oauth/menu/${pk}/`, data)
    },

    // 删除菜单
    deleteMenu: function (pk) {
        return http.delete(`/oauth/menu/${pk}/`)
    },

    // 获取角色
    getRole: function () {
        return http.get('/oauth/role/', {})
    },

    // 新增角色
    createRole: function (data) {
        return http.post('/oauth/role/', data)
    },

    // 更新角色
    updateRole: function (pk, data) {
        return http.put(`/oauth/role/${pk}/`, data)
    },

    // 删除角色
    deleteRole: function (pk) {
        return http.delete(`/oauth/role/${pk}/`)
    },

    test: function () {
        http.get('/oauth/test', {})
    },

    routerName: function () {
        return http.get('/oauth/router_name/', {})
    },

    // 获取角色个人信息
    getUserPersonal: function (user_id) {
        return http.get(`/oauth/user_personal/${user_id}/combo_info/`, {})
    },

}
