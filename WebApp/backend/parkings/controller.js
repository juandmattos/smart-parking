const pool = require('../db')
const {
  allParkingsQuery,
  makeDBQuery,
  deleteParkingsQuery,
  getParkingsInfoQuery
} = require('./queries')
const { makeParkingsJSON } = require('../utils')

// GET URL/api/v1/parkings/
const getParkings = (_, res) => {
  pool.query(allParkingsQuery, (error, results) => {
    if (error) throw error
  
    const parkings = makeParkingsJSON(results.rows)
    res.status(200).json(parkings)
  })
}

// POST URL/api/v1/parkings/
  // First --> clean DB table parkings
  // Second --> Update with new values
const updateDB = (req, res) => {
  const query = makeDBQuery(req.body)

  pool.query(deleteParkingsQuery, (error, _) => {
    if (error) throw error
    pool.query(query, (error, _) => {
      if (error) throw error
      res.status(200).json({ message: 'Database Updated!' })
    })
  })
}

const getParkingsInfo = (_, res) => {
  pool.query(getParkingsInfoQuery, (error, results) => {
    if (error) throw error
  
    res.status(200).json(results.rows)
  })
}

module.exports = {
  getParkings,
  updateDB,
  getParkingsInfo
}
