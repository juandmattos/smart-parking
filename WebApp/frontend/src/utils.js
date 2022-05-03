const MAKE_IT_REAL_TIME = false

const getOccupationDescription = (occ) => {
  switch(occ){
    case 'low':
      return 'Relativamente Libre'
    case 'mid':
      return 'Relativamente Ocupado' 
    case 'high':
      return 'Muy Ocupado'
    default:
      return 'No hay información'       
  }
}

const getNumberOfSpots = (levels) => {
  let freeSpaces = 0
  let totalSpaces = 0

  levels.forEach((level) => {
    const spaces = getNumberOfSpotFromArea(level.areas)
    freeSpaces = freeSpaces + spaces[0]
    totalSpaces = totalSpaces + spaces[1]
  })

  return [freeSpaces, totalSpaces]
}

// state is false ==> Spot is Free
// state is true  ==> Spot is Taken
const getNumberOfSpotFromArea = (areas) => {
  let freeSpaces = 0
  let totalSpaces = 0

  areas.forEach((area) => {
    area.slots.forEach((slot) => {
      totalSpaces += 1
      if (!slot.state) {
        freeSpaces += 1
      }
    })
  })

  return [freeSpaces, totalSpaces]
}


export {
  getOccupationDescription,
  getNumberOfSpotFromArea,
  getNumberOfSpots,
  MAKE_IT_REAL_TIME
}