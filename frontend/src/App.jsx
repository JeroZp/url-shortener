import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Stats from './pages/Stats.jsx'

function App() {
  return (
    <div className="container">
      <h1>URL Shortener</h1>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/stats/:shortCode" element={<Stats />} />
      </Routes>
    </div>
  )
}

export default App
