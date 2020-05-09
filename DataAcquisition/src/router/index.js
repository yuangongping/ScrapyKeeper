import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

/* Layout */
import Layout from '../views/Layout/Layout'

export const constantRouterMap = [
  { path: '/404', component: () => import('@/views/404'), hidden: true },
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
    children: [{
      path: 'project',
      name: 'project',
      component: () => import('@/views/Project/Project.vue'),
      meta: { title: '项目管理', icon: 'list', roles: ['leader'] }
    }]
  },
  {
    path: '',
    component: Layout,
    children: [
      {
        path: 'machine',
        name: 'machine',
        component: () => import('@/views/Machine/Machine'),
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
  },
  {
    path: '',
    component: Layout,
    children: [{
      path: 'templates',
      name: 'templates',
      component: () => import('@/views/Templates/Templates'),
      meta: { title: '模板管理', icon: 'visual', roles: ['leader'] }
    }]
  }
]

