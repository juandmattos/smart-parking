import React from 'react'
import { Link } from 'react-router-dom'
import {
  getOccupationDescription,
  getWording,
  EMPTY,
  ALMOST_EMPTY,
  ALMOST_FULL,
  FULL,
} from '../../utils'
import classes from './LevelItem.module.css'

const LevelItem = ({ level, parkingId }) => {

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

  return (
    <div
      className={`${classes.container} ${getClass(level.level_occupation)}`}
    >
      <div className={classes.info}>
        <span className={classes.levelArea}>
          <Link 
            to={`/parkings/${parkingId}/${level['level_id']}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            <h2>{level.level_name}</h2>
          </Link>
        </span>
        <div>
          <span className={classes.desc}>
            {getOccupationDescription(level.level_occupation)}
          </span>
        </div>
      </div>
      <div className={classes.spotInfo}>
        <div>
          <span className={classes.price}>
            {getWording(level.areas, false)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default LevelItem
