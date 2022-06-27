import React from 'react'
import { useParams, useLocation } from 'react-router-dom'
import SpotList from '../components/jparkings/SpotList'

const SpotDetail = () => {
  const { parkingId, levelId, areaId } = useParams()
  const { state } = useLocation()
  return (
    <SpotList
      areaId={areaId}
      parkingId={parkingId}
      levelId={levelId}
      dynamicPrice={state?.dynamicPrice}
    />
  )
}

export default SpotDetail
