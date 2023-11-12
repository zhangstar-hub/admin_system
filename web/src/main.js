import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import http from './http'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import utils from '@/utils/directives';

const app = createApp(App)
app.config.globalProperties.$http = http;
app.use(store).use(router).use(ElementPlus, {
    locale: zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.directive('permControl', utils.permControl);

app.mount('#app')
