const groupBy = (array, key) => {
  return array.reduce((result, currentValue) => {
    (result[currentValue[key]] = result[currentValue[key]] || []).push(
      currentValue
    )
    return result;
  }, {})
}

const makeParkingsJSON = (results) => {
  const aux = []
  results.forEach(({parking_id, level_id, area_id, slot_id, state, price}) => {
    aux.push({
      parking_id,
      slot: {
        id: `${level_id}-${area_id}`,
        name: slot_id,
        state,
        price
      }
    })
  })
  return groupBy(aux, 'parking_id')
}

module.exports = {
  makeParkingsJSON
}