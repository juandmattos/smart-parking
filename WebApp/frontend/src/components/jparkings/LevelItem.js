import React from 'react'
import { Link } from 'react-router-dom'
import { getOccupationDescription, getWording} from '../../utils'
import classes from './LevelItem.module.css'

const LevelItem = ({ level, parkingId }) => {

  const getClass = (occupation) => {
    switch(occupation){
      case 'low':
        return classes.free
      case 'mid':
        return classes.mid  
      case 'high':
        return classes.used  
      default:
        return ''      
    }
  }

  return (
    <div
      className={`${classes.container} ${getClass(level.occupation)}`}
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
            <h2>{level.name}</h2>
          </Link>
        </span>
        <div>
          <span className={classes.desc}>
            {getOccupationDescription(level.occupation)}
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
