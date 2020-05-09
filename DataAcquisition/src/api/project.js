import request from '@/utils/request'
const querystring = require('querystring')

export function getAllProject(page_index, page_szie) {
  return request({
    url: '/project',
    method: 'get',
    params: { page_index, page_szie }
  })
}

export function apiEditProjectInfo(form) {
  return new Promise((resolve, reject) => {
    request({
      url: '/project',
      method: 'put',
      data: querystring.stringify(form)
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}

export function delProject(form) {
  return request({
    url: '/project',
    method: 'delete',
    data: querystring.stringify({
      id: form.id,
      project_name: form.project_name
    })
  })
}

export function apiAddProject(form) {
  return new Promise((resolve, reject) => {
    request({
      url: '/project',
      method: 'post',
      data: querystring.stringify(form)
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}
