import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import classes from './SummaryParking.module.css'
import LoadingSpinner from '../UI/LoadingSpinner'
import SummaryArea from './SummaryArea'
import { getIndividualParking } from '../../api/apiParking'
import { MAKE_IT_REAL_TIME } from '../../utils'

const SummaryParking = ({ parkingId }) => {
  const [parking, setParking] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualParking(parkingId)
        setIsLoading(false)
        setParking(response.data)
        setError(false)
      } catch (err) {
        setError(true)
      }
    }
    fetch()
    // eslint-disable-next-line
  }, [])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualParking(parkingId)
        setIsLoading(false)
        setParking(response.data)
        setError(false)
      } catch (err) {
        console.log(err)
        setError(true)
      }
    }
    if (MAKE_IT_REAL_TIME) {
      const interval = setInterval(() => fetch(), 5000)
      return () => clearInterval(interval)
    }
    // eslint-disable-next-line
  }, [])

  if (error) {
    return (
      <section className={classes.container}>
        <div className={classes.centered}>
          <h2>Un error ocurrió buscando el parking..</h2>
        </div>
      </section>
    )
  }

  if (isLoading && !error) {
    return (
      <section className={classes.container}>
        <div className={classes.centered}>
          <LoadingSpinner />
        </div>
      </section>
    )
  }

  if (parking.length === 0) {
    return (
      <section className={classes.container}>
        <div className={classes.centered}>
          <h2>No se encontro el parking seleccionado..</h2>
        </div>
      </section>
    )
  }

  return (
    <section className={classes.container}>
      <h1>{parking.parking_name}</h1>
      <h5><i>{parking.parking_description}, {parking.parking_address}</i></h5>
      <Link 
          to={`/`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          {`< Volver`}
      </Link>
      <hr
        style={{
            color: 'white',
            backgroundColor: 'white',
            width: '65%',
            height: 1,
            marginBottom: '2rem'
        }}
      />
      {parking.levels.map((level, index) => (
        <div className={classes.levelContainer} key={index}>
          <h4 className={classes.levelHeader}>
            {level.level_name}
          </h4>
          <div className={classes.flex}>
            {level.areas.map((area, ind) => (
              <SummaryArea
                area={area}
                key={ind}
                level={level}
                parkingId={parkingId}
                ind={ind}
                parkingSummary={parking.parking_summary}
              />
            ))}
          </div>
        </div>
      ))}
    </section>
  )
}

export default SummaryParking
