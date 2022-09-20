import React from 'react'
import ReactTooltip from 'react-tooltip'
import { Link } from 'react-router-dom'
import { FaInfoCircle } from 'react-icons/fa'
import classes from './SummaryParking.module.css'
import {
  getOccupationDescription,
  getDynamicPrice,
  getWording,
  isLabor,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
} from '../../utils'

const getClass = (occupation, occupation_percentage) => {
  if (!occupation_percentage) {
    switch(occupation){
      case EMPTY:
        return classes.free
      case ALMOST_EMPTY:
        return classes.free  
      case ALMOST_FULL:
        return classes.mid  
      case FULL:
        return classes.used  
      default:
        return ''      
    }
  } else {
    const occ = Math.floor(occupation_percentage/10)
    switch (occ) {
      case 0:
      case 1:
      case 2:
      case 3:
      case 4:
        return classes.free
      case 5:
      case 6:
      case 7:
        return classes.mid
      case 8:
      case 9:
      case 10:
        return classes.used
      default:
        return classes.free
    }
  }
}

const areaSummary = (hasFreeHours, freeHourUntil, monthFee, isHoliday, holidayType) => (
  <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
    <div>
      Horas Gratis: {hasFreeHours ? freeHourUntil : 'No tiene'}
    </div>
    <div>
      Precio por Mes: ${monthFee}
    </div>
    {isHoliday ? (
      <div>
        {`Al ser feriado ${isLabor(holidayType)}, los precios pueden variar`}
      </div>
    ) : null}
  </div>
)

const SummaryArea = ({ area, level, parkingId, ind, parkingSummary, parkingDisabled, parkingIsHoliday, parkingHolidayType }) => {
  return (
    <div className={`${classes.areaContainer} ${getClass(area.area_occupation, area.area_occupation_percentage)}`}>
      <div className={classes.info}>
        <span className={classes.levelArea}>
          {parkingDisabled ? (
            <p className={classes.disabled}>Sector {area.area_name} - (Deshabilitado/Cerrado)</p>
          ) : (
            <Link
              to={{
                pathname: `/parkings/${parkingId}/${level.level_id}/${area['area_id']}`,
              }}
              state={{dynamicPrice: getDynamicPrice(parkingSummary, area.area_summary, area.area_id, level.level_id, area.area_occupation_percentage)}}
              style={{
                color: 'inherit',
                textDecoration: 'inherit'
              }}
            >
              <h2>Sector {area.area_name}</h2>
            </Link>
          )}
        </span>
        <div
        style={{
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <div style={{ fontSize: '0.7rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <b style={{ marginRight: '0.4rem' }}>Color:</b>
            <span
              className={classes.defaultDot}
              style={{ backgroundColor: area.area_color }}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <p className={classes.desc}>
              {getOccupationDescription(area.area_occupation, area.area_occupation_percentage)}
            </p>
          </div>
          <span className={classes.averagePrice} style={{ marginTop: '0.3rem' }}>
            <p data-tip data-for={`info-${area.area_id}-${ind}`} style={{ cursor: 'pointer' }}>
              <FaInfoCircle size='12px' />
            </p>
            <ReactTooltip id={`info-${area.area_id}-${ind}`}>
              {areaSummary(area.area_summary.hasFreeHours, area.area_summary.freeHourUntil, area.area_summary.monthFee, parkingIsHoliday, parkingHolidayType)}
            </ReactTooltip>
          </span>
        </div>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.availableSpots}>
            {getWording([area], false)}
          </span>
          <br />
          <span className={classes.price}>
            {`Precio Sector: $${getDynamicPrice(parkingSummary, area.area_summary, area.area_id, level.level_id, area.area_occupation_percentage)} la hora`}
          </span>
        </div>
      </div>
    </div>    
  )
}

export default SummaryArea
