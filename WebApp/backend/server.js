const express = require('express')
const cors = require('cors')
const dotenv = require('dotenv')
const parkingRoutes = require('./parkings/routes')
const weatherRoutes = require('./weather/routes')
const parkingJSONRoutes = require('./parkingsJSON/routes')

dotenv.config({path: __dirname + '/.env'})
const app = express()
const PORT = process.env.PORT || 5005

app.use(cors())
app.use(express.json())

app.use('/api/v1/parkings/', parkingRoutes)
app.use('/api/v1/weather/', weatherRoutes)

app.use('/api/v1/jparkings/', parkingJSONRoutes)

app.listen(PORT, () => console.log(`Listening on port ${PORT}..`))
