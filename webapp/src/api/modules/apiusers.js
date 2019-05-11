import { HTTP, encodeQueryData } from '@/api'

export default {
  getUsers (cb, ecb, query) {
    let data = {}
    data.page = query.page
    data.per_page = query.perPage
    let queryString = encodeQueryData(data)
    HTTP.get('users' + queryString)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  getUser (cb, ecb, id) {
    HTTP.get('users/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  postUsers (cb, ecb, user) {
    HTTP.post('users', user)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  putUser (cb, ecb, user) {
    HTTP.put('users/' + user.id, user)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  patchUser (cb, ecb, user) {
    HTTP.patch('users/' + user.id, user)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  deleteUser (cb, ecb, id) {
    HTTP.delete('users/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  }
}
