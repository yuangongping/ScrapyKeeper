import request from '@/utils/request'
const querystring = require('querystring')

export function apidRunImmediately(id) {
  return request({
    url: '/scheduler',
    method: 'get',
    params: { id }
  })
}

export function apidCancleRunning(id) {
  return new Promise((resolve, reject) => {
    request({
      url: '/scheduler',
      method: 'put',
      data: querystring.stringify({ id: id })
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}

export function apiAddScheduler(form) {
  return new Promise((resolve, reject) => {
    request({
      url: '/scheduler',
      method: 'post',
      data: querystring.stringify(form)
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}

export function apiCancelScheduler(project_id) {
  return request({
    url: '/scheduler',
    method: 'delete',
    data: querystring.stringify({
      project_id: project_id
    })
  })
}
