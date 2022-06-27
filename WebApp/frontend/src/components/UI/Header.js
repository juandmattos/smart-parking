import moment from 'moment'
import { Link } from 'react-router-dom'
import parkingImage from '../../assets/parking.jpg'
import classes from './Header.module.css'

const Header = ({weather, isLoading}) => {
  const getTime = () => {
    moment.locale('es');
    return moment().format('dddd, h a, MMMM Do YYYY')
  }

  return (
    <>
      <header className={classes.header}>
        <h1>
          <Link 
            to={`/`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            Parking APP
          </Link>
        </h1>
        <div className={classes.weatherContainer}>
          <p><b>Clima:</b></p>
          <p><i>{isLoading ? <span>Loading...</span> : <span>{weather}</span>}</i></p>
        </div>
        <div>
          <Link 
            to={`/about`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >
            Conoce el proyecto
          </Link>
          <h5 style={{ margin: 0, marginTop: '0.5rem' }}>{getTime()}</h5>
        </div>
      </header>
      <div className={classes['main-image']}>
        <img src={parkingImage} alt='parking app' />
      </div>
    </>
  )
}

export default Header
