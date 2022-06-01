import React from 'react'
import classes from './SpotItem.module.css'

const SpotItem = ({ spot }) => (
  <div
    className={`${classes.container} ${spot.slot_state ? classes.used : classes.free}`}
  >
    <div className={classes.info}>
      <span className={classes.levelArea}>
        <h2>Lugar {spot['slot_id']}</h2>
      </span>
      <div>
        <span className={classes.desc}>
          {spot.slot_state ? 'Ocupado' : 'Libre'}
        </span>
      </div>
    </div>
    <div className={classes.spotInfo}>
      <div>
        <span className={classes.price}>
          Precio: ${spot.slot_price}
        </span>
      </div>
    </div>
  </div>
)

export default SpotItem

