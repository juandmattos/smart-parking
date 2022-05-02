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

const getParking = (req, res) => {
  const id = req.params.parkingId
  pool.query(getParkingQuery, (error, results) => {
    if (error) throw error

    const parking = results.rows[0].parkings.find(ele => ele['parking_id'] === id)
    if (!parking) {
      return res.status(200).json([])
    }
    res.status(200).json(parking)
  })
}

const getLevel = (req, res) => {
  const parkingid = req.params.parkingId
  const levelId = req.params.levelId
  pool.query(getParkingQuery, (error, results) => {
    if (error) throw error

    const parking = results.rows[0].parkings.find(ele => ele['parking_id'] === parkingid)
    if (!parking) {
      return res.status(200).json([])
    } else {
      const level = parking.levels.find(ele => ele['level_id'] === levelId)
      if (!level) {
        return res.status(200).json([])
      }
      res.status(200).json(level)
    }
  })
}

const getArea = (req, res) => {
  const parkingid = req.params.parkingId
  const levelId = req.params.levelId
  const areaId = req.params.areaId
  pool.query(getParkingQuery, (error, results) => {
    if (error) throw error

    const parking = results.rows[0].parkings.find(ele => ele['parking_id'] === parkingid)
    if (!parking) {
      return res.status(200).json([])
    } else {
      const level = parking.levels.find(ele => ele['level_id'] === levelId)
      if (!level) {
        return res.status(200).json([])
      } else {
        const area = level.areas.find(ele => ele['area_id'] === areaId)
        if (!area) {
          return res.status(200).json([])
        }
        res.status(200).json(area)
      }
    }
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
  getParking,
  getLevel,
  getArea,
  getParkings,
  updateJSONDB
}
