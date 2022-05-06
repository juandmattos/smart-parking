const { Router } = require('express')
const {
  getParkings,
  updateJSONDB,
  getParking,
  getLevel,
  getArea
} = require('./controller')

const router = Router()

router.get('/', getParkings)
router.get('/:parkingId', getParking)
router.get('/:parkingId/:levelId', getLevel)
router.get('/:parkingId/:levelId/:areaId', getArea)
router.post('/', updateJSONDB)

module.exports = router
