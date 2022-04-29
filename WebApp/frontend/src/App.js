import { useState, useEffect } from 'react'
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom'
import Header from './components/UI/Header'

import Parkings from './pages/Parkings'
import NotFound from './pages/NotFound'
import Detail from './pages/Detail'
import About from './pages/About'

import { getWeather } from './api/apiWeather'

function App() {
  const [weather, setWeather] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getWeather()
        const data = response.data.weather
        setWeather(`${data.charAt(0).toUpperCase()}${data.slice(1)}`)
        setIsLoading(false)
      } catch (error) {
      }
    }
    fetch()
  }, [])

  return (
    <Router>
      <Header weather={weather} isLoading={isLoading} />
      <main>
        <Routes>
          <Route
              path='/'
              element={<Navigate to='/parkings' replace />}
          />
          <Route path='/parkings' element={<Parkings />} />
          <Route path='/parkings/:parkingId' element={<Detail />} />
          <Route path='/about' element={<About />} />
          <Route path='/notfound' element={<NotFound />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
