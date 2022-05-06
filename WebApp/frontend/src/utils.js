const MAKE_IT_REAL_TIME = true

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

const getWording = (list, isLevel) => {
  let freeSpots = 0
  let allSpots = 0
  if (isLevel) {
    [freeSpots, allSpots] = getNumberOfSpots(list)
  } else {
    [freeSpots, allSpots] = getNumberOfSpotFromArea(list)
  }
  let wording = ''

  if (freeSpots === 1) {
    wording = `1 lugar disponible de ${allSpots}`
  } else {
    wording = `${freeSpots} lugares disponibles de ${allSpots}`
  }
  return wording
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
  getWording,
  MAKE_IT_REAL_TIME
}