import React from 'react'
import ReactTooltip from 'react-tooltip'
import { Link } from 'react-router-dom'
import { FaInfoCircle } from 'react-icons/fa'
import classes from './SummaryParking.module.css'
import {
  getOccupationDescription,
  getDynamicPrice,
  getWording,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
} from '../../utils'

const getClass = (occupation) => {
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
}

const areaSummary = (hasFreeHours, freeHourUntil, monthFee) => (
  <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
    <div>
      Horas Gratis: {hasFreeHours ? freeHourUntil : 'No tiene'}
    </div>
    <div>
      Precio por Mes: ${monthFee}
    </div>
    <div></div>
  </div>
)

const SummaryArea = ({ area, level, parkingId, ind, parkingSummary }) => {
  return (
    <div className={`${classes.areaContainer} ${getClass(area.area_occupation)}`}>
      <div className={classes.info}>
        <span className={classes.levelArea}>
          <Link
            to={`/parkings/${parkingId}/${level.level_id}/${area['area_id']}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            <h2>Sector {area.area_name}</h2>
          </Link>
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
              {getOccupationDescription(area.area_occupation)}
            </p>
          </div>
          <span className={classes.averagePrice} style={{ marginTop: '0.3rem' }}>
            <p data-tip data-for={`info-${area.area_id}-${ind}`} style={{ cursor: 'pointer' }}>
              <FaInfoCircle size='12px' />
            </p>
            <ReactTooltip id={`info-${area.area_id}-${ind}`}>
              {areaSummary(area.area_summary.hasFreeHours, area.area_summary.freeHourUntil, area.area_summary.monthFee)}
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
            {/* TODO - Make DYNAMIC */}
            {`Precio Promedio: $${getDynamicPrice(parkingSummary, area.area_summary, area.area_id, level.level_id)} la hora`}
          </span>
        </div>
      </div>
    </div>    
  )
}

export default SummaryArea
