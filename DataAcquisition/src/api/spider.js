import request from '@/utils/request'
const querystring = require('querystring')

// 获取所有蜘蛛运行情况
export function getAllSpider(pageIndex, pageSize) {
  return request({
    url: '/allspider',
    method: 'get',
    params: { pageIndex, pageSize }
  })
}

export function addScheduler(form) {
  form['selectedmonths'] = form['selectedmonths'].length === 0 ? null : form['selectedmonths'].join(',')
  form['selecteddays'] = form['selecteddays'].join(',').length === 0 ? null : form['selecteddays'].join(',')
  form['selectedhours'] = form['selectedhours'].join(',').length === 0 ? null : form['selectedhours'].join(',')
  form['selectedminutes'] = form['selectedminutes'].join(',').length === 0 ? null : form['selectedminutes'].join(',')
  return request({
    url: '/addscheduler',
    method: 'post',
    data: querystring.stringify(form)
  })
}

export function delScheduler(job_instance_id) {
  return request({
    url: '/delscheduler',
    method: 'get',
    params: {
      job_instance_id
    }
  })
}

export function runOnce(project_id, spider_name) {
  return request({
    url: '/runonce',
    method: 'post',
    data: querystring.stringify({
      project_id: project_id,
      spider_name: spider_name,
      spider_arguments: '',
      daemon: 'auto',
      priority: 0
    })
  })
}

export function apiCancelspider(project_id, project_name, job_instance_id) {
  return new Promise((resolve, reject) => {
    request({
      url: '/cancelspider',
      method: 'post',
      data: querystring.stringify({
        project_id: project_id,
        project_name: project_name,
        job_instance_id: job_instance_id
      })
    }).then((res) => {
      resolve(res)
    }).catch((e) => {
      reject(e)
    })
  })
}

export function getMasterLog(project_id, job_exec_id) {
  return request({
    url: '/masterlog',
    method: 'get',
    params: {
      project_id,
      job_exec_id
    }
  })
}

export function getSlaveLog(project_id, job_exec_id) {
  return request({
    url: '/slavelog',
    method: 'get',
    params: {
      project_id,
      job_exec_id
    }
  })
}
