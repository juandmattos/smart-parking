import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import AreaItem from './AreaItem'
import Card from '../UI/Card'
import classes from './AreaList.module.css'
import { getIndividualLevel } from '../../api/apiParking'
import { MAKE_IT_REAL_TIME } from '../../utils'

const AreaList = props => {
  const [areas, setAreas] = useState([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualLevel(props.parkingId, props.levelId)
        setAreas(response.data.areas)
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
        const response = await getIndividualLevel(props.parkingId, props.levelId)
        setAreas(response.data.areas)
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
        <h1>Areas del Parking</h1>
        <Link 
          to={`/parkings/${props.parkingId}`}
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
              {areas.map((ele, index) => (
                <AreaItem key={index} area={ele} parkingId={props.parkingId} levelId={props.levelId} />
              ))}
            </div>
          </div>
        </Card>
      </section>
    </>
  )
}

export default AreaList
