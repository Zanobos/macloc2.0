import axios from 'axios'

export const BASE_URL = process.env.BE_SERVER
export const SOCKET_IO_NAMESPACE = 'api/climbs'
export const SOCKET_IO_PATH = '/api/socket.io'
export const STATIC_URL = BASE_URL + 'api/static/'
export const SOCKET_IO_URL = BASE_URL + SOCKET_IO_NAMESPACE

export const HTTP = axios.create({
  baseURL: BASE_URL + 'api/'
})

export function encodeQueryData (data) {
  let ret = []
  for (let d in data) {
    if (data[d] != null) {
      ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]))
    }
  }
  return '?' + ret.join('&')
}

export function defaultErrorHandler (error) {
  console.log('error during remote call:')
  console.log(error)
}

export function getWallImg (imageId) {
  return STATIC_URL + 'walls/' + imageId
}
