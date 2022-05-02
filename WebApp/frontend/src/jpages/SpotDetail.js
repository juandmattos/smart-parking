import React from 'react'
import { useParams } from 'react-router-dom'
import SpotList from '../components/jparkings/SpotList'

const SpotDetail = () => {
  const { areaId } = useParams()
  console.log(areaId)
  return (
    <SpotList />
  )
}

export default SpotDetail
