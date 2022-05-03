import React from 'react'
import { Link } from 'react-router-dom'
import { getNumberOfSpotFromArea} from '../../utils'
import classes from './AreaItem.module.css'

const AreaItem = ({ area, parkingId, levelId }) => {
  return (
    <div
      className={`${classes.container}`}
    >
      <div className={classes.info}>
        <span className={classes.levelArea}>
          <Link 
            to={`/parkings/${parkingId}/${levelId}/${area['area_id']}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            <h2>Sector {area.name}</h2>
          </Link>
        </span>
        <div>
          <span className={classes.desc}>
            {area.description}
          </span>
        </div>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.price}>
            {getNumberOfSpotFromArea([area])[0]} lugares disponibles de {getNumberOfSpotFromArea([area])[1]}
          </span>
        </div>
      </div>
    </div>
  )
}

export default AreaItem

