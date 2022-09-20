import axios from 'axios'
import { PARKING_API_CODE } from '../utils'

const { REACT_APP_BASE_URL } = process.env

const client = axios.create({
  baseURL: REACT_APP_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

// API CALLS
const getParkingJSON = () => client.get(`/api/v1/${PARKING_API_CODE}/`)
const getIndividualParking = (parkingId) => client.get(`/api/v1/${PARKING_API_CODE}/${parkingId}`)
const getIndividualLevel = (parkingId, levelId) => client.get(`/api/v1/${PARKING_API_CODE}/${parkingId}/${levelId}`)
const getIndividualArea = (parkingId, levelId, areaId) => client.get(`/api/v1/${PARKING_API_CODE}/${parkingId}/${levelId}/${areaId}`)

export {
  getParkingJSON,
  getIndividualParking,
  getIndividualLevel,
  getIndividualArea
}
