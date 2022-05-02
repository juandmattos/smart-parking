import React from 'react'
import { useParams } from 'react-router-dom'
import AreaList from '../components/jparkings/AreaList'

const AreaDetail = () => {
  const { levelId } = useParams()
  console.log(levelId)
  return (
    <AreaList />
  )
}

export default AreaDetail
