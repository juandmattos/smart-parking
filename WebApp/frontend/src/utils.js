import { FaCar, FaTruck, FaMotorcycle } from 'react-icons/fa'

const MAKE_IT_REAL_TIME = false

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

const getIcon = (type) => {
  switch(type) {
    case 'cars':
      return <FaCar size='20px' />
    case 'trucks':
      return <FaTruck size='20px' />
    case 'motorcycles':
      return <FaMotorcycle size='20px' />        
    default:
      return <FaCar size='20px' />
  }
}

const occupationDiccionary = (occupation) => {
  switch (occupation) {
    case 0:
    case 1:
      return '0to20Coef'
    case 2:
    case 3:
      return '20to40Coef'
    case 4:
    case 5:
      return '40to60Coef'
    case 6:
    case 7:
      return '60to80Coef'
    case 8:
    case 9:
    case 10:
      return '80to100Coef'
    default:
      return '0to20Coef'
  }
}

const getEstimatedOccupation = (levels, areaId, levelId) => {
  console.log()
  const level = levels.find(l => l.level_id === levelId)
  if (!level){
    return -1
  } else {
    const foundArea = level.areas.find(a => a.area_id === areaId)
    if (!foundArea) {
      return -1
    } else {
      return foundArea.area_occupation_percentage_target
    }
  }
}

const getDynamicPrice = (parkingSummary, aSummary, areaId, levelId) => {
  if (!parkingSummary.hasDynamicPrice) {
    return aSummary.hourFee
  } else {
    const estimatedOccupation = getEstimatedOccupation(parkingSummary.levels, areaId, levelId)
    if (estimatedOccupation === -1) {
      return aSummary.hourFee
    } else {
      const occupationKey = occupationDiccionary(Math.floor(estimatedOccupation/10))
      const dynamicCoeff = parkingSummary.coefficients[occupationKey]
      if (!dynamicCoeff) {
        return aSummary.hourFee
      }
      return dynamicCoeff*aSummary.hourFee
    }
  }
}

export {
  getOccupationDescription,
  getWording,
  getIcon,
  getDynamicPrice,
  MAKE_IT_REAL_TIME,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
  PARKING_API_CODE
}
