import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

export const constantRouterMap = [
  { path: '/404', component: () => import('@/views/404'), hidden: true },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'root',
    hidden: true
  }
]

export default new Router({

  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

export const asyncRouterMap = [
  {
    path: '',
    redirect: '/project',
    hidden: true
  },
  {
    path: '',
    component: Layout,
    name: '项目管理',
    children: [{
      path: 'project',
      name: '项目管理',
      component: () => import('@/views/project/index.vue'),
      meta: { title: '项目管理', icon: 'list', roles: ['leader'] }
    }]
  },
  {
    path: '',
    component: Layout,
    name: '参数配置',
    children: [
      {
        path: 'machine',
        name: '节点',
        component: () => import('@/views/machine/index'),
        meta: { title: '节点', icon: 'server', roles: ['leader'] }
      }
    ]
  },
  {
    path: '',
    component: Layout,
    children: [{
      path: 'data',
      name: 'data',
      component: () => import('@/views/DataCenter/DataCenter'),
      meta: { title: '数据中心', icon: 'log', roles: ['leader'] }
    }]
  }
]

