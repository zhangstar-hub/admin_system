import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: ()=>import('@/views/LoginView'),
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
        meta: {'isShow': false}
      },
      {
        path: '/',
        name: 'admin',
        icon: 'Tools',
        children: [
          {
            path: 'user',
            name: 'user',
            component: ()=>import('@/views/admin/UserView'),
          },
          {
            path: 'role',
            name: 'role',
            component: ()=>import('@/views/admin/RoleView'),
          },
          {
            path: 'permission',
            name: 'permission',
            component: ()=>import('@/views/admin/PermissionView'),
          },
          {
            path: 'menu',
            name: 'menu',
            component: ()=>import('@/views/admin/MenuView'),
          },
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
  next()
})


export default router
