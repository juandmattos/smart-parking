import axios from 'axios'

const { REACT_APP_BASE_URL } = process.env

const client = axios.create({
  baseURL: REACT_APP_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

const getParkings = () => client.get(`/api/v1/parkings/`)
const getParkingsInfo = () => client.get(`/api/v1/parkings/info`)

export {
  getParkings,
  getParkingsInfo
}
