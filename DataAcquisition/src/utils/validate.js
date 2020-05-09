/**
 * Created by jiachenpan on 16/11/18.
 */

export function isvalidUsername(name) {
    if (name === '') {
      return false
    }
    var invalidQuote = '[`~!@#$^&*()=|{}:;\',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“。，、？] '
    var status = true
    for (var i = 0; i < name.length; i++) {
      if (invalidQuote.indexOf(name[i]) >= 0) {
        status = false
        break
      }
    }
    return status
  }
  
  // 验证邮箱
  export function isvalidEmail(email) {
    var reg = new RegExp('^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$')
    if (email === '') {
      return false
    } else if (!reg.test(email)) {
      return false
    } else {
      return true
    }
  }
  
  // 验证工程名
  export function isvalidProjName(projname) {
    const reg = /^[A-Za-z0-9]+$/
    return reg.test(projname)
  }
  
  /* 合法uri*/
  export function validateURL(textval) {
    const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
    return urlregex.test(textval)
  }
  
  /* 小写字母*/
  export function validateLowerCase(str) {
    const reg = /^[a-z]+$/
    return reg.test(str)
  }
  
  /* 大写字母*/
  export function validateUpperCase(str) {
    const reg = /^[A-Z]+$/
    return reg.test(str)
  }
  
  /* 大小写字母*/
  export function validateAlphabets(str) {
    const reg = /^[A-Za-z]+$/
    return reg.test(str)
  }
  