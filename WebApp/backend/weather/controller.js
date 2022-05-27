const fetch = require('node-fetch')
const path = require('path')
require('dotenv').config({ path: path.resolve(__dirname, '../.env') })
const localLat = '-34.894708'
const localLong = '-56.155346'
const {
  WEATHER_API_URL,
  WEATHER_API_KEY
} = process.env
const weatherUrl = `${WEATHER_API_URL}?lat=${localLat}&lon=${localLong}&appid=${WEATHER_API_KEY}&lang=sp&units=metric`

async function getWeather() {
  const response = await fetch(weatherUrl);
  return response.json();
}

const getLocalWeather = (_, res) => {
  getWeather().then(data => {
    const description = data.weather[0].description
    const temperature = data.main.temp
    const humidity = data.main.humidity
    return res.send({
      weather: `${description} con una temperatura de ${temperature}°C y una humedad de ${humidity}%`
    })
  }).catch(err => {
    console.log(err)
  })
}

module.exports = {
  getLocalWeather,
}
