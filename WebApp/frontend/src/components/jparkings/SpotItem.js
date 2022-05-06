import React from 'react'
// import { Link } from 'react-router-dom'
import classes from './SpotItem.module.css'

const SpotItem = ({ spot, parkingId, levelId, areaId }) => {
  return (
    <div
      className={`${classes.container} ${spot.state ? classes.used : classes.free}`}
    >
      <div className={classes.info}>
        <span className={classes.levelArea}>
          {/* <Link 
            to={`/parkings/${parkingId}/${levelId}/${areaId}/${spot['slot_id']}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          > */}
          <h2>Lugar {spot['slot_id']}</h2>
          {/* </Link> */}
        </span>
        <div>
          <span className={classes.desc}>
            {spot.state ? 'Ocupado' : 'Libre'}
          </span>
        </div>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.price}>
            Precio: ${spot.price}
          </span>
        </div>
      </div>
    </div>
  )
}

export default SpotItem

