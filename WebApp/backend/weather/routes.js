const { Router } = require('express')
const { getLocalWeather } = require('./controller')
const router = Router()

router.get('/', getLocalWeather)

module.exports = router
