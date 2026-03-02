import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import VoiceTransaction from './pages/VoiceTransaction'
import PriceIntelligence from './pages/PriceIntelligence'
import FreshnessScanner from './pages/FreshnessScanner'
import Marketplace from './pages/Marketplace'
import TrustScore from './pages/TrustScore'
import Tutorial from './components/Tutorial'
import { DemoModeProvider, useDemoMode } from './contexts/DemoModeContext'

function AppContent() {
  const { showTutorial, setShowTutorial } = useDemoMode()

  return (
    <>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/voice" element={<VoiceTransaction />} />
          <Route path="/prices" element={<PriceIntelligence />} />
          <Route path="/freshness" element={<FreshnessScanner />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/trust-score" element={<TrustScore />} />
        </Routes>
      </div>
      {showTutorial && (
        <Tutorial
          onComplete={() => setShowTutorial(false)}
          onSkip={() => setShowTutorial(false)}
        />
      )}
    </>
  )
}

function App() {
  return (
    <Router>
      <DemoModeProvider>
        <AppContent />
      </DemoModeProvider>
    </Router>
  )
}

export default App
