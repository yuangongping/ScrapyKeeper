import request from '@/utils/request'
const querystring = require('querystring')

export function getAllProject(page_index, page_szie) {
  return request({
    url: '/template',
    method: 'get',
    params: { page_index, page_szie }
  })
}

//编辑模板
export function apiEditModel(form) {
    return new Promise((resolve, reject) => {
      request({
        url: '/template',
        method: 'put',
        data: querystring.stringify(form)
      }).then((res) => {
        resolve(res)
      }).catch((e) => {
        reject(e)
      })
    })
  }

// 删除模板
export function delModel(id) {
    return request({
      url: '/template',
      method: 'delete',
      data: querystring.stringify({
        id: id
      })
    })
  }
//获取模板列表
export function apiGetModel(params) {
    return new Promise((resolve, reject) => {
      request({
        url: '/template',
        method: 'get',
        params: params
      }).then((res) => {
        resolve(res)
      }).catch((e) => {
        reject(e)
      })
    })
  }
//添加模板
export function apiAddModel(form) {
  return new Promise((resolve, reject) => {
    request({
      url: '/template',
      method: 'post',
      data: querystring.stringify(form)
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}