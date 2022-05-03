import React from 'react'
import { useParams } from 'react-router-dom'
import SpotList from '../components/jparkings/SpotList'

const SpotDetail = () => {
  const { parkingId, levelId, areaId } = useParams()
  return (
    <SpotList areaId={areaId} parkingId={parkingId} levelId={levelId} />
  )
}

export default SpotDetail
