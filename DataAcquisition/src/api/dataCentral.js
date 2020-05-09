import request from '@/utils/request'
const querystring = require('querystring')

export function apiGetStatus() {
  return request({
    url: '/data_central',
    method: 'get',
  })
}

export function apiGetProjectWeekData() {
  return request({
    url: '/data_central',
    method: 'post',
  })
}