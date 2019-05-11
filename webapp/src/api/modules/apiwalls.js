import { HTTP, encodeQueryData } from '@/api'

export default {
  getWalls (cb, ecb, query) {
    let data = {}
    data.page = query.page
    data.per_page = query.perPage
    let queryString = encodeQueryData(data)
    HTTP.get('walls' + queryString)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  getWall (cb, ecb, id) {
    HTTP.get('walls/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  postWalls (cb, ecb, wall) {
    HTTP.post('walls', wall)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  putWall (cb, ecb, wall) {
    HTTP.put('walls/' + wall.id, wall)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  patchWall (cb, ecb, wall) {
    HTTP.patch('walls/' + wall.id, wall)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  },
  deleteWall (cb, ecb, id) {
    HTTP.delete('walls/' + id)
      .then(
        (response) => cb(response),
        (error) => ecb(error)
      )
  }
}
