const getParkingQuery = `
  select parkings
  from parkings_json
`

const makeDBQuery = (body) => {
  const updateDBQuery = `
    insert into 
      parkings_json(parkings)
    values
      ('${JSON.stringify(body)}')
  `
  return updateDBQuery
}

const deleteParkingsQuery = `delete from parkings_json`

module.exports = {
  getParkingQuery,
  makeDBQuery,
  deleteParkingsQuery,
}