import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SpotItem from './SpotItem'
import Card from '../UI/Card'
import classes from './SpotList.module.css'
import { getIndividualArea } from '../../api/apiParking'
import { MAKE_IT_REAL_TIME } from '../../utils'

const SpotList = props => {
  const [spots, setSpots] = useState([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualArea(props.parkingId, props.levelId, props.areaId)
        setSpots(response.data.slots)
      } catch (error) {
        console.log(error)
      }
    }
    fetch()
    // eslint-disable-next-line
  }, [])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualArea(props.parkingId, props.levelId, props.areaId)
        setSpots(response.data.slots)
      } catch (error) {
        console.log(error)
      }
    }
    if (MAKE_IT_REAL_TIME) {
      const interval = setInterval(() => fetch(), 5000)
      return () => clearInterval(interval)
    }
    // eslint-disable-next-line
  }, [])

  return (
    <>
      <section className={classes.centered}>
        <h1>Lugares del Parking</h1>
        <div className={classes.linkContainer}>
          <Link
            to={`/parkings/summary/${props.parkingId}`}
            style={{
              color: 'inherit',
              textDecoration: 'inherit'
            }}
          >        
            <p className={classes.back}>
              {`< Volver a pantalla completa`}
            </p>
          </Link>
        </div>
      </section>
      <section className={classes.spots}>
        <Card>
          <div>
            <div className={classes.container}>
              {spots.map((ele, index) => (
                <SpotItem
                  key={index} 
                  spot={ele} 
                  parkingId={props.parkingId}
                  levelId={props.levelId}
                  areaId={props.areaId}
                  dynamicPrice={props.dynamicPrice}
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
