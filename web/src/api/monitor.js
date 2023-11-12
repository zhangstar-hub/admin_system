import http from "@/http";

export default {

    // 短信数据监控
    smsMonitor: function (data) {
        return http.get('/oauth/sms_monitor/', {params: data});
    },

    // test 短信发送
    smsSend: function (data) {
        return http.post('/oauth/sms_progress/', {num: data});
    },

    // test 短信进度监听
    smsProgress: function () {
        return http.get('/oauth/sms_progress/');
    },

    // 获取Sms
    getSms: function () {
        return http.get('/oauth/sms/', {})
    },

    // 新增Sms
    createSms: function (data) {
        return http.post('/oauth/sms/', data)
    },

    // 更新Sms
    updateSms: function (pk, data) {
        return http.put(`/oauth/sms/${pk}/`, data)
    },

    // 删除Sms
    deleteSms: function (pk) {
        return http.delete(`/oauth/sms/${pk}/`)
    },

    // 删除Sms
    liveShowSms: function (id_list) {
        return http.post(`/oauth/sms/live_show/`, {'id_list': id_list})
    },
}
