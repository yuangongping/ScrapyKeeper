import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css'// progress bar style
import { getUsername, removeAllCookies } from '@/utils/auth' // getToken from cookie

NProgress.configure({ showSpinner: false })// NProgress Configuration

const whiteList = ['/login']// no redirect whitelist
router.beforeEach((to, from, next) => {
  NProgress.start() // start progress bar
  // 取用户名
  if (getUsername()) {
    // 取路由
    if (store.getters.routerState === 'setted') {
      next()
    } else {
      // 取角色
      const roles = 'admin,developer'
      // const roles = getRoles()
      // 有角色，构造路由
      if (roles.length > 0) {
        store.dispatch('GenerateRoutes', roles).then(() => { // 根据roles权限生成可访问的路由表
          router.addRoutes(store.getters.addRouters) // 动态添加可访问路由表
          store.commit('SET_ROUTER_STATE', 'setted')
          next({ ...to, replace: true })
        })
      } else {
        // 没有角色，重定向到首页
        Message.info('未获取到角色信息，请登录！')
        removeAllCookies()
        window.location = process.env.BACKEND_URL
      }
    }
  } else {
    // 没有取到用户名，清除cookie，重定向到首页
    if (whiteList.indexOf(to.path) !== -1) { // 在免登录白名单，直接进入
      next()
    } else {
      Message.info('未获取到登录信息，请登录！')
      removeAllCookies()
      window.location = process.env.BACKEND_URL
    }
  }
})

router.afterEach(() => {
  NProgress.done() // finish progress bar
})
