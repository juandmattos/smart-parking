const pool = require('../db')

const {
  getParkingQuery,
  makeDBQuery,
  deleteParkingsQuery,
} = require('./queries')

const getParkings = (_, res) => {
  pool.query(getParkingQuery, (error, results) => {
    if (error) throw error

    res.status(200).json(results.rows[0].parkings)
  })
}

const updateJSONDB = (req, res) => {
  const query = makeDBQuery(req.body)

  pool.query(deleteParkingsQuery, (error, _) => {
    if (error) throw error
    pool.query(query, (error, _) => {
      if (error) throw error
      res.status(200).json({ message: 'Database Updated!' })
    })
  })
}

module.exports = {
  getParkings,
  updateJSONDB
}
