import React from 'react'
import classes from './SpotItem.module.css'

const SpotItem = props => {
  // state is false ==> Spot is Free
  // state is true  ==> Spot is Taken
  const {
    id: levelArea,
    name,
    price,
    state: isTaken
  } = props.spot

  return (
    <div
      className={`${classes.container} ${!isTaken ? `${classes.free}` : `${classes.used}`}`}
    >
      <div className={classes.info}>
        <span className={classes.levelArea}>
          <h4>Nivel-Area:</h4>{levelArea}
        </span>
        <p><b>Lugar: </b>{name}</p>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.desc}>{!isTaken ? 'Lugar Disponible' : 'Lugar Ocupado'}</span>
        </div>
        <div>
          <span className={classes.price}>{`$${price}`}</span>
        </div>
      </div>
    </div>
  )
}

export default SpotItem
