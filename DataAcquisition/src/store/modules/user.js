import { regist, login, getInfo } from '@/api/user'
import { getToken, setToken, removeToken, getRoles } from '@/utils/auth'
import { removeAllCookies } from '../../utils/auth'

const user = {
  state: {
    token: getToken(),
    name: '',
    avatar: '',
    email: '',
    roles: getRoles()
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_EMAIL: (state, email) => {
      state.email = email
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      const username = userInfo.username.trim()
      return new Promise((resolve, reject) => {
        login(username, userInfo.password).then(response => {
          const data = response.data
          setToken(data.token)
          commit('SET_TOKEN', data.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 注册
    Regist({ commit }, userInfo) {
      const username = userInfo.username.trim()
      const email = userInfo.email.trim()
      return new Promise((resolve, reject) => {
        regist(username, email, userInfo.password).then(response => {
          if (response.data.message === 'existed') {
            resolve('existed')
          } else {
            const data = response.data
            setToken(data.token)
            commit('SET_TOKEN', data.token)
            resolve()
          }
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo(state.token).then(response => {
          const data = response.data
          if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
            commit('SET_ROLES', data.roles)
          } else {
            reject('getInfo: roles must be a non-null array !')
          }
          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_EMAIL', data.email)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      removeAllCookies()
      const logoutUrl = process.env.BACKEND_URL + '/logout/'
      window.location = logoutUrl
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user
