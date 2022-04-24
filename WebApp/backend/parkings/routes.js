const { Router } = require('express')
const { getParkings, updateDB, getParkingsInfo } = require('./controller')

const router = Router()

router.get('/', getParkings)
router.get('/info', getParkingsInfo)
router.post('/', updateDB)

module.exports = router
