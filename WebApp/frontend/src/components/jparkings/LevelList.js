import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import LevelItem from './LevelItem'
import Card from '../UI/Card'
import classes from './LevelList.module.css'
import { getIndividualParking } from '../../api/apiParking'
import { MAKE_IT_REAL_TIME } from '../../utils'

const LevelList = props => {
  const [levels, setLevels] = useState([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualParking(props.parkingId)
        setLevels(response.data.levels)
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
        const response = await getIndividualParking(props.parkingId)
        setLevels(response.data.levels)
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
        <h1>Pisos del Parking</h1>
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
              {levels.map((ele, index) => (
                <LevelItem
                  key={index}
                  level={ele}
                  parkingId={props.parkingId}
                />
              ))}
            </div>
          </div>
        </Card>
      </section>
    </>
  )
}

export default LevelList
