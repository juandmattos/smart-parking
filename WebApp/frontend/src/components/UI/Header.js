import { Link } from 'react-router-dom'
import parkingImage from '../../assets/parking.jpg'
import classes from './Header.module.css'

const Header = () => {
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
        <p>
          Clima: Soleado 25 grados (IN PROGRESS)
        </p>
        <Link 
          to={`/about`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          About
        </Link>
      </header>
      <div className={classes['main-image']}>
        <img src={parkingImage} alt='parking app' />
      </div>
    </>
  )
}

export default Header
