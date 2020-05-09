import request from '@/utils/request'
const querystring = require('querystring')


export function apiStartUrl(form) {
  return new Promise((resolve, reject) => {
    request({
      url: 'start_urls',
      method: 'post',
      data: querystring.stringify(form)
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}