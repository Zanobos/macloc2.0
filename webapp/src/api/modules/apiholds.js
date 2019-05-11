import { HTTP, encodeQueryData } from '@/api'

export default {
  getHolds (cb, ecb, query) {
    let data = {}
    data.wall_id = query.wallId
    data.page = query.page
    data.per_page = query.perPage
    let queryString = encodeQueryData(data)
    HTTP.get('holds' + queryString)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  getHold (cb, ecb, id) {
    HTTP.get('holds/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  postHolds (cb, ecb, hold) {
    HTTP.post('holds', hold)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  putHold (cb, ecb, hold) {
    HTTP.put('holds/' + hold.id, hold)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  patchHold (cb, ecb, hold) {
    HTTP.patch('holds/' + hold.id, hold)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  deleteHold (cb, ecb, id) {
    HTTP.delete('holds/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  }
}
