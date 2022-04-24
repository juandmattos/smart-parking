import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom'
import Header from './components/UI/Header'

import Parkings from './pages/Parkings'
import NotFound from './pages/NotFound'
import Detail from './pages/Detail'
import About from './pages/About'

function App() {
  return (
    <Router>
      <Header />
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
