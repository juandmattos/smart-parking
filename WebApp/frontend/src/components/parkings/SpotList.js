import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SpotItem from './SpotItem'
import Card from '../UI/Card'
import classes from './SpotList.module.css'
import { getParkings } from '../../api/apiParking'

const SpotList = props => {
  const [spots, setSpots] = useState([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getParkings()
        setSpots(response.data[props.parkingId])
      } catch (error) {
        console.log(error)
      }
    }
    fetch()
  }, [])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getParkings()
        setSpots(response.data[props.parkingId])
      } catch (error) {
        console.log(error)
      }
    }
    const interval = setInterval(() => fetch(), 5000);
    return () => clearInterval(interval);
  }, [])

  return (
    <>
      <section className={classes.centered}>
        <h1>Lugares del Parking</h1>
        <Link 
          to={`/`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >        
          <p className={classes.back}>
            {`< Volver`}
          </p>
        </Link>
      </section>
      <section className={classes.spots}>
        <Card>
          <div>
            <div className={classes.container}>
              {spots.map((ele, index) => (
                <SpotItem
                  key={index}
                  spot={ele.slot}
                />
              ))}
            </div>
          </div>
        </Card>
      </section>
    </>
  )
}

export default SpotList
