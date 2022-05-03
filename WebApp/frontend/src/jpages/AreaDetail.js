import React from 'react'
import { useParams } from 'react-router-dom'
import AreaList from '../components/jparkings/AreaList'

const AreaDetail = () => {
  const { parkingId, levelId } = useParams()
  return (
    <AreaList parkingId={parkingId} levelId={levelId} />
  )
}

export default AreaDetail
