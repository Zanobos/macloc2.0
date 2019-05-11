import { HTTP, encodeQueryData } from '@/api'

export default {
  getClimbs (cb, ecb, query) {
    let data = {}
    data.status = query.status
    data.not_status = query.not_status
    data.user_id = query.userId
    data.page = query.page
    data.per_page = query.perPage
    let queryString = encodeQueryData(data)
    HTTP.get('climbs' + queryString)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  getClimb (cb, ecb, id) {
    HTTP.get('climbs/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  postClimbs (cb, ecb, climb, query) {
    let data = {}
    data.wall_id = query.wallId
    data.user_id = query.userId
    let queryString = encodeQueryData(data)
    HTTP.post('climbs' + queryString, climb)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  putClimb (cb, ecb, climb) {
    HTTP.put('climbs/' + climb.id, climb)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  patchClimb (cb, ecb, climb) {
    HTTP.patch('climbs/' + climb.id, climb)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  deleteClimb (cb, ecb, id) {
    HTTP.delete('climbs/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  }
}
