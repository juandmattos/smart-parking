import React from 'react'
import { useParams } from 'react-router-dom'
import LevelList from '../components/jparkings/LevelList'

const LevelDetail = () => {
  const { parkingId } = useParams()
  return (
    <LevelList parkingId={parkingId} />
  )
}

export default LevelDetail
