import React from 'react'
import { useParams } from 'react-router-dom'
import SpotList from '../components/parkings/SpotList'

const Detail = () => {
  const { parkingId } = useParams()
  return (
    <SpotList parkingId={parkingId} />
  )
}

export default Detail
