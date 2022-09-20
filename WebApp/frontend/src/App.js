import { useState, useEffect, lazy, Suspense } from 'react'
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom'
import Header from './components/UI/Header'
import LoadingSpinner from './components/UI/LoadingSpinner'
import { MAKE_IT_REAL_TIME } from './utils'
import { getWeather } from './api/apiWeather'

const Parkings = lazy(() => import('./jpages/Parkings'))
const LevelDetail = lazy(() => import('./jpages/LevelDetail'))
const AreaDetail = lazy(() => import('./jpages/AreaDetail'))
const SpotDetail = lazy(() => import('./jpages/SpotDetail'))
const SummaryParking = lazy(() => import('./jpages/SummaryPage'))
const About = lazy(() => import('./jpages/About'))
const NotFound = lazy(() => import('./jpages/NotFound'))

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
    <Suspense
      fallback={
        <div className='centeredSpinner'>
          <LoadingSpinner />
        </div>
      }
    >
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
            <Route path='/parkings/summary/:parkingId' element={<SummaryParking />} />
            <Route path='/about' element={<About />} />
            <Route path='/notfound' element={<NotFound />} />
            <Route path='*' element={<NotFound />} />
          </Routes>
        </main>
      </Router>
    </Suspense>
  )
}

export default App
