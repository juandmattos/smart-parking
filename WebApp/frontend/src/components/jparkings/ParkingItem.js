import { Link } from 'react-router-dom'
import { getWording } from '../../utils'
import classes from './ParkingItem.module.css'

const ParkingItem = (props) => (
  <li className={classes.parking}>
    <div style={{ width: '100%' }}>
      {props.disabled ? (
        <h3 className={classes.disabled}>{props.name} - (Deshabilitado/Cerrado)</h3>
      ) : (
        <Link
          to={`/parkings/summary/${props.id}`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          <h3>{props.name}</h3>
        </Link>
      )}
      <div className={classes.description}>
        {props.description}
      </div>
      {!props.disabled && (
        <div className={classes.info}>
          <div className={classes.floor}>
            Pisos: {props.levels}
          </div>
          <div className={classes.spot}>
            <i>{getWording(props.levelList, true)}</i>
          </div>
        </div>
      )}
      {!props.disabled && (
        <div className={classes.info}>
          <br/>
          <Link
            to={`/parkings/${props.id}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            <i className={classes.summaryLink}>{`Ver info individual del parking`}</i>
          </Link>
        </div>
      )}
      <div className={classes.timestamp}>
        {`La última actualización fue: ${props.timestamp}`}
      </div>
    </div>
  </li>
)

export default ParkingItem
