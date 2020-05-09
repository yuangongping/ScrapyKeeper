import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getUsername() {
  return 'admin'
  // return Cookies.get('username')
}

export function getRoles() {
  let roles = Cookies.get('roles')
  if (roles) {
    roles = roles.replace(/\\054/g, ',')
    return roles.split(',')
  } else {
    return null
  }
}

export function removeAllCookies() {
  for (const key in Cookies.get()) {
    Cookies.remove(key)
  }
}
