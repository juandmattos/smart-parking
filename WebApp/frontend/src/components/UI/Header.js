import { Link } from 'react-router-dom'
import parkingImage from '../../assets/parking.jpg'
import classes from './Header.module.css'

const Header = ({weather, isLoading}) => {
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
        <Link 
          to={`/about`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          Conoce el proyecto
        </Link>
      </header>
      <div className={classes['main-image']}>
        <img src={parkingImage} alt='parking app' />
      </div>
    </>
  )
}

export default Header
