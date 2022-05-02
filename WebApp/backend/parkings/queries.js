const allParkingsQuery = `
  select parking_id, level_id, area_id, slot_id, state, price 
  from parkings 
  group by parking_id, level_id, area_id, slot_id, state, price
  order by parking_id
`

const makeDBQuery = (body) => {
  const updateDBQuery = `
    insert into 
      parkings(parking_id, level_id, area_id, slot_id, state, price)
    values
      ${body.map(({parking_id, level_id, area_id, slot_id, state, price}) => 
        `(\'${parking_id}\',\'${level_id}\',\'${area_id}\',\'${slot_id}\',\'${state}\',\'${price}\')`)}
  `
  return updateDBQuery
}

const deleteParkingsQuery = `delete from parkings`

const getParkingsInfoQuery = `select * from parking_info order by parking_id`

module.exports = {
  allParkingsQuery,
  makeDBQuery,
  deleteParkingsQuery,
  getParkingsInfoQuery
}