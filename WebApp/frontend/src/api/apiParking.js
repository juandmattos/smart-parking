import axios from 'axios'

const { REACT_APP_BASE_URL } = process.env

const client = axios.create({
  baseURL: REACT_APP_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

const getParkingJSON = () => client.get(`/api/v1/jparkings/`)
const getIndividualParking = (parkingId) => client.get(`/api/v1/jparkings/${parkingId}`)
const getIndividualLevel = (parkingId, levelId) => client.get(`/api/v1/jparkings/${parkingId}/${levelId}`)
const getIndividualArea = (parkingId, levelId, areaId) => client.get(`/api/v1/jparkings/${parkingId}/${levelId}/${areaId}`)

export {
  getParkingJSON,
  getIndividualParking,
  getIndividualLevel,
  getIndividualArea
}
