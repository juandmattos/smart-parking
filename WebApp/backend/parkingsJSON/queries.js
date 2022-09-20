const getParkingQuery = `select parkings from parkings_json`
const deleteParkingsQuery = `delete from parkings_json`
const makeDBQuery = (body) => `insert into parkings_json(parkings) values ('${JSON.stringify(body)}')`

module.exports = {
  getParkingQuery,
  makeDBQuery,
  deleteParkingsQuery,
}
