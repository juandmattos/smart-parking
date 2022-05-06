import React, { useState, useEffect } from 'react'
import Card from '../UI/Card'
import LoadingSpinner from '../UI/LoadingSpinner'
import ParkingItem from './ParkingItem'
import classes from './AvailableParkings.module.css'
import { getParkingJSON } from '../../api/apiParking'

const AvailableParkings = props => {
  const [parkings, setParkings] = useState([]);
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getParkingJSON()
        setIsLoading(false)
        setParkings(response.data)
        setError(false)
      } catch (error) {
        setError(true)
      }
    }
    fetch()
  }, [])


  if (error) {
    <section className={classes.parkingsLoading}>
      <div className={classes.centered}>
        Un error ocurrió buscando los parkings..
      </div>
    </section>
  }

  if (isLoading && !error) {
    return (
      <section className={classes.parkingsLoading}>
        <div className={classes.centered}>
          <LoadingSpinner />
        </div>
      </section>
    )
  }

  if (parkings.length === 0) {
    return (
      <section className={classes.parkingsLoading}>
        <div className={classes.centered}>
          No hay parkings en la app..
        </div>
      </section>
    )
  }

  const parkingsList = parkings.map((parking, index) => (
    <ParkingItem
      key={`${parking.parking_id}-${index}`}
      id={parking.parking_id}
      name={parking.name}
      description={parking.description}
      spots={parking.spots}
      levels={parking.levels?.length || 0}
      levelList={parking.levels || []}
      disabled={parking.disabled}
    />
  ))

  return (
    <section className={classes.parkings}>
      <Card>
        <ul>{parkingsList}</ul>
      </Card>
    </section>
  )
}

export default AvailableParkings
