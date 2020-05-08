import request from '@/utils/request'
const querystring = require('querystring')

export function regist(username, email, password) {
  return request({
    url: '/regist',
    method: 'post',
    data: querystring.stringify({
      username,
      email,
      password
    })
  })
}

export function login(username, password) {
  return request({
    url: '/sys/log',
    method: 'post',
    data: querystring.stringify({
      username,
      password
    })
  })
}

export function getInfo(token) {
  return request({
    url: '/userinfo',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'get'
  })
}
export function getCollectDataInfo(from) {
  return request({
    url: 'collect_data_info',
    method: 'post',
    data: querystring.stringify({
      manager_person: from['manager_person'],
      start_date: from['start_date'],
      end_date: from['end_date'],
      pageIndex: from['pageIndex'],
      pageSzie: from['pageSize']
    })
  })
}
