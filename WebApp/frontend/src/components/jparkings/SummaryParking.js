import React, { useState, useEffect } from 'react'
import classes from './SummaryParking.module.css'
import LoadingSpinner from '../UI/LoadingSpinner'
import { getIndividualParking } from '../../api/apiParking'
import { MAKE_IT_REAL_TIME } from '../../utils'

const SummaryParking = ({ parkingId }) => {
  const [parkings, setParkings] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualParking(parkingId)
        setIsLoading(false)
        setParkings(response.data)
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
        setParkings(response.data)
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

  if (parkings.length === 0) {
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
      <h2>PANTALLA COMPLETA</h2>
    </section>
  )
}

export default SummaryParking
