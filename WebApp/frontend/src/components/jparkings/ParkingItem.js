import { Link } from 'react-router-dom'
import classes from './ParkingItem.module.css'

const ParkingItem = (props) => {

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
            Lugares Totales: {props.spots}
          </div>
        </div>
      </div>
    </li>
  )
}

export default ParkingItem
