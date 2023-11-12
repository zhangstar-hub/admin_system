import store from '@/store';
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView'),
    meta: {
      noAuth: true
    }
  },
  {
    path: '/',
    name: 'main',
    component: ()=>import('@/views/MainView'),
    children: [
      {
        path: 'home',
        name: 'home',
        component: () => import('@/views/HomeView'),
        meta: { 'isShow': false }
      },
      {
        path: '/',
        name: 'admin',
        icon: 'Tools',
        children: [
          {
            path: 'user',
            name: 'user',
            component: () => import('@/views/admin/UserView'),
          },
          {
            path: 'role',
            name: 'role',
            component: () => import('@/views/admin/RoleView'),
          },
          {
            path: 'permission',
            name: 'permission',
            component: () => import('@/views/admin/PermissionView'),
          },
          {
            path: 'menu',
            name: 'menu',
            component: () => import('@/views/admin/MenuView'),
          },
        ]
      },
      {
        path: '/',
        name: 'monitor',
        icon: 'TrendCharts',
        children: [
          {
            path: 'smsMonitor',
            name: 'smsMonitor',
            component: () => import('@/views/monitor/SmsMonitorView'),
          },
          {
            path: 'smsSender',
            name: 'smsSender',
            component: () => import('@/views/monitor/SmsSenderView'),
          }
        ]
      },
      {
        path: '/',
        name: 'back',
        icon: 'HelpFilled',
        children: [
          {
            path: 'back1',
            name: 'back1',
            component: ()=>import('@/views/back/BackView1'),
          },
          {
            path: 'back2',
            name: 'back2',
            component: ()=>import('@/views/back/BackView2'),
          },
          {
            path: 'back3',
            name: 'back3',
            component: ()=>import('@/views/back/BackView3'),
          },
        ]
      },
      {
        path: '/',
        name: 'front',
        icon: 'StarFilled',
        children: [
          {
            path: 'front1',
            name: 'front1',
            component: ()=>import('@/views/front/FrontView1'),
          },
          {
            path: 'front2',
            name: 'front2',
            component: ()=>import('@/views/front/FrontView2'),
          },
          {
            path: 'front3',
            name: 'front3',
            component: ()=>import('@/views/front/FrontView3'),
          },
        ]
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token') || null;
  if (!token && !to.meta.noAuth) {
    next({name: 'login'});
  } else {
    store.commit('menu/updateMenuHistroy', to)
    next()
  }
})


export default router
