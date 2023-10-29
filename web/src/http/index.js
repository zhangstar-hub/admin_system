import axios from "axios";
import { ElMessage } from "element-plus";
import store from "@/store";
import router from "@/router";

const http = axios.create({
  baseURL: '/api',
  timeout: 1000                   //请求超时设置，单位ms
})

http.interceptors.request.use(
  function (config) {  
    config.headers.AUTHORIZATION = 'token ' + store.state.user.token;
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  function (response) {return response},
  function (error) {
    console.log(error);
    let err_message = error.response.data.detail;
    for (const m of err_message) {
        ElMessage.error(m)
    }
    if (error.response.status === 401) {
      store.commit("user/clearAll");
      router.push({'name': 'login'})
    }
    return Promise.reject(error);
});

export default http
