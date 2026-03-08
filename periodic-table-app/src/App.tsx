import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom'
import './App.css'
import PeriodicTable from './components/PeriodicTable'
import ElementDetail from './pages/ElementDetail'
import type { Element } from './data/elements'

function HomePage() {
  const navigate = useNavigate()

  const handleElementClick = (element: Element) => {
    navigate(`/element/${element.atomicNumber}`)
  }

  return (
    <div className="home-page">
      <header className="app-header">
        <h1>Mendeleev's Periodic Table</h1>
        <p className="app-subtitle">Click on any element to view its 3D atomic model</p>
      </header>
      <main className="app-main">
        <PeriodicTable onElementClick={handleElementClick} />
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/element/:atomicNumber" element={<ElementDetail />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
