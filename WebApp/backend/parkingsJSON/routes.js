const { Router } = require('express')
const { getParkings, updateJSONDB } = require('./controller')

const router = Router()

router.get('/', getParkings)
router.post('/', updateJSONDB)

module.exports = router
