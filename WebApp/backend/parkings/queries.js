const getParkingsQuery = `select parking_json from parkings`
const getParkingQuery = (id) => `select parking_json from parkings where parking_external_id = ${id}`
const insertParking = 
  (external_id, body) => `insert into parkings(parking_external_id, parking_json) values ('${external_id}', '${JSON.stringify(body)}')`
const updateParking =
  (external_id, body) => `update parkings set parking_json=('${JSON.stringify(body)}') where parking_external_id=${external_id}`

module.exports = {
  getParkingsQuery,
  getParkingQuery,
  insertParking,
  updateParking
}
