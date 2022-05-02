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
        <div className={classes.spot}>
          Lugares: {props.spots}
        </div>
      </div>
    </li>
  )
}

export default ParkingItem
