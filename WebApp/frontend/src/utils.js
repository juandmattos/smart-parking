import { FaCar, FaTruck, FaMotorcycle } from 'react-icons/fa'

const MAKE_IT_REAL_TIME = true

const EMPTY = 'Empty'
const ALMOST_EMPTY = 'Almost Empty'
const ALMOST_FULL = 'Almost Full'
const FULL = 'Full'

const PARKING_API_CODE = 'parkings'

const OCCUPATION_TOLERANCE = 10;

const getOccupationDescription = (occ, occupation_percentage) => {
  if (!occupation_percentage) {
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
  } else {
    const occupation = Math.floor(occupation_percentage/10)
    switch (occupation) {
      case 0:
        return 'Libre'
      case 1:
      case 2:
      case 3:
      case 4:
        return 'Relativamente Libre'
      case 5:
      case 6:
      case 7:
        return 'Relativamente Ocupado'
      case 8:
      case 9:
        return 'Muy Ocupado'
      case 10:
        return 'No hay lugar'
      default:
        return 'Relativamente Libre'
    }
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

/**
 * '0to20Coef'
 * '20to40Coef'
 * '40to60Coef'
 * '60to80Coef'
 * '80to100Coef'
 * 
 */

const occupationDiccionary = (occupation) => {
  switch (occupation) {
    case 0:
    case 1:
    case 2:
      return '0to20Coef'
    case 3:
    case 4:
      return '20to40Coef'
    case 5:
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

const getDynamicPrice = (parkingSummary, aSummary, areaId, levelId, areaOccupationLive) => {
  if (!parkingSummary.hasDynamicPrice) {
    return aSummary.hourFee
  } else {
    const estimatedOccupation = getEstimatedOccupation(parkingSummary.levels, areaId, levelId)
    if (estimatedOccupation === -1) {
      return aSummary.hourFee
    } else {
      const toleranceDiff = Math.abs(+estimatedOccupation - +areaOccupationLive)
      let occupationKey = 0
      if (toleranceDiff <= OCCUPATION_TOLERANCE) {
        occupationKey = occupationDiccionary(Math.floor(estimatedOccupation/10))
      } else {
        occupationKey = occupationDiccionary(Math.floor(areaOccupationLive/10))
      }
      const dynamicCoeff = parkingSummary.coefficients[occupationKey]
      if (!dynamicCoeff) {
        return aSummary.hourFee
      }
      return dynamicCoeff*aSummary.hourFee
    }
  }
}

const isLabor = (holidayType) => {
  if (holidayType === 'L') {
    return 'Laborable'
  }
  return 'No Laborable'
}

export {
  getOccupationDescription,
  getWording,
  getIcon,
  getDynamicPrice,
  isLabor,
  MAKE_IT_REAL_TIME,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
  PARKING_API_CODE
}
