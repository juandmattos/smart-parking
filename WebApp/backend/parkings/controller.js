const pool = require('../db')

const {
  getParkingsQuery,
  getParkingQuery,
  insertParking,
  updateParking
} = require('./queries')

const getParkings = (_, res) => {
  pool.query(getParkingsQuery, (error, results) => {
    if (error) throw error
    const response = []
    results.rows.forEach(row => response.push(row['parking_json']))

    res.status(200).json(response)
  })
}

const getParking = (req, res) => {
  pool.query(getParkingQuery(req.params.parkingId), (error, results) => {
    if (error) throw error
    if (results.rows.length === 0) {
      return res.status(404).json({message: 'Not Found'})
    }
    return res.status(200).json(results.rows[0].parking_json)
  })
}

const getLevel = (req, res) => {
  const parkingid = req.params.parkingId
  const levelId = req.params.levelId
  pool.query(getParkingQuery(parkingid), (error, results) => {
    if (error) throw error

    const parking = results.rows[0].parking_json
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
  pool.query(getParkingQuery(parkingid), (error, results) => {
    if (error) throw error

    const parking = results.rows[0].parking_json
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

const upsertParking = async (req, res) => {
  const parkingId = req.params.externalId
  pool.query(getParkingQuery(parkingId), (error, results) => {
    if (error) throw error
    if (results.rows.length === 0) {
      pool.query(insertParking(parkingId, req.body), (err, _) => {
        if (err) throw err
        return res.status(200).json({message: 'inserted'})
      })
    } else {
      pool.query(updateParking(parkingId, req.body), (err, _) => {
        if (err) throw err
        return res.status(200).json({message: 'updated'})
      })
    }
  })
}

module.exports = {
  getParkings,
  getParking,
  getLevel,
  getArea,
  upsertParking
}
