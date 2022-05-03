import { Link } from 'react-router-dom'
import { getNumberOfSpots } from '../../utils'
import classes from './ParkingItem.module.css'

const ParkingItem = (props) => {

  console.log(props.levelList)

  return (
    <li className={classes.parking}>
      <div>
        <Link 
          to={`/parkings/${props.id}`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          <h3>{props.name}</h3>
        </Link>
        <div className={classes.description}>
          {props.description}
        </div>
        <div className={classes.info}>
          <div className={classes.spot}>
            Pisos: {props.levels}
          </div>
          <div className={classes.spot}>
            /
          </div>
          <div className={classes.spot}>
            {getNumberOfSpots(props.levelList)[0]} lugares disponibles de {getNumberOfSpots(props.levelList)[1]}
          </div>
        </div>
      </div>
    </li>
  )
}

export default ParkingItem
