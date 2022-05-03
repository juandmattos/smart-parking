import { useState, useEffect } from 'react'
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom'
import Header from './components/UI/Header'

import Parkings from './jpages/Parkings'
import LevelDetail from './jpages/LevelDetail'
import AreaDetail from './jpages/AreaDetail'
import SpotDetail from './jpages/SpotDetail'
import About from './jpages/About'
import NotFound from './jpages/NotFound'

import { MAKE_IT_REAL_TIME } from './utils'

import { getWeather } from './api/apiWeather'

  // state is false ==> Spot is Free
  // state is true  ==> Spot is Taken
  
function App() {
  const [weather, setWeather] = useState('')
  const [isLoading, setIsLoading] = useState(false)

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
    if (MAKE_IT_REAL_TIME) {
      fetch()
    }
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
          <Route path='/parkings/:parkingId' element={<LevelDetail />} />
          <Route path='/parkings/:parkingId/:levelId' element={<AreaDetail />} />
          <Route path='/parkings/:parkingId/:levelId/:areaId' element={<SpotDetail />} />
          <Route path='/about' element={<About />} />
          <Route path='/notfound' element={<NotFound />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
