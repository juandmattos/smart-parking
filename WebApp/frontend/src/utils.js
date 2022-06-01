const MAKE_IT_REAL_TIME = true

const EMPTY = 'Empty'
const ALMOST_EMPTY = 'Almost Empty'
const ALMOST_FULL = 'Almost Full'
const FULL = 'Full'

const PARKING_API_CODE = 'parkings'

const getOccupationDescription = (occ) => {
  switch(occ) {
    case EMPTY:
      return 'Relativamente Libre'
    case ALMOST_EMPTY:
      return 'Relativamente Libre'
    case ALMOST_FULL:
      return 'Relativamente Ocupado' 
    case FULL:
      return 'Muy Ocupado'
    default:
      return 'No hay información'       
  }
}

// state is false ==> Spot is Free
// state is true  ==> Spot is Taken
const getWording = (list, isLevel) => {
  let freeSpots = 0
  let allSpots = 0
  list.forEach(item => {
    if (isLevel) {
      allSpots = allSpots + parseInt(item.level_total_spots)
      freeSpots = freeSpots + parseInt(item.level_available_spots)
    } else {
      allSpots = allSpots + parseInt(item.area_total_spots)
      freeSpots = freeSpots + parseInt(item.area_available_spots)
    }
  })
  let wording = ''

  if (freeSpots === 1) {
    wording = `1 lugar disponible de ${allSpots}`
  } else {
    wording = `${freeSpots} lugares disponibles de ${allSpots}`
  }
  return wording
}

export {
  getOccupationDescription,
  getWording,
  MAKE_IT_REAL_TIME,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
  PARKING_API_CODE
}