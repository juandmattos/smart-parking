import React from 'react'
import { Link } from 'react-router-dom'
import { getWording } from '../../utils'
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
            <h2>Sector {area.area_name}</h2>
          </Link>
        </span>
        <div>
          <span className={classes.desc}>
            {area.area_description}
          </span>
        </div>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.price}>
            {getWording([area], false)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default AreaItem

