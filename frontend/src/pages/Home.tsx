import { Link, useNavigate } from 'react-router-dom'
import { DEMO_CREDENTIALS } from '../config/api'
import { useDemoMode } from '../contexts/DemoModeContext'

function Home() {
  const navigate = useNavigate()
  const { isDemoMode, toggleDemoMode, setShowTutorial, offlineQueue } = useDemoMode()

  const handleVoiceClick = () => {
    navigate('/voice')
  }

  const handleRestartTutorial = () => {
    setShowTutorial(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-3 sm:py-4">
          <h1 className="text-xl sm:text-2xl font-bold text-primary-700">Smart Vendors</h1>
          <p className="text-xs sm:text-sm text-gray-600">Voice-First Decision Intelligence</p>
        </div>
      </header>

      {/* Demo Credentials Banner */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 mx-4 mt-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3 flex-1">
            <p className="text-xs sm:text-sm text-yellow-700">
              <strong>Demo:</strong> <code className="bg-yellow-100 px-1 sm:px-2 py-1 rounded text-xs">{DEMO_CREDENTIALS.username}</code> / <code className="bg-yellow-100 px-1 sm:px-2 py-1 rounded text-xs">{DEMO_CREDENTIALS.password}</code>
            </p>
          </div>
        </div>
      </div>

      {/* Demo Mode Toggle and Tutorial */}
      <div className="mx-4 mt-4 flex gap-2">
        <button
          onClick={toggleDemoMode}
          className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
            isDemoMode
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          {isDemoMode ? '✓ Demo Mode' : 'Demo Mode'}
        </button>
        <button
          onClick={handleRestartTutorial}
          className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg font-medium hover:bg-blue-200 transition-colors"
        >
          Tutorial
        </button>
      </div>

      {/* Offline Queue Indicator */}
      {offlineQueue.length > 0 && (
        <div className="mx-4 mt-4 bg-orange-50 border-l-4 border-orange-400 p-3">
          <p className="text-sm text-orange-700">
            <strong>{offlineQueue.length}</strong> transaction{offlineQueue.length > 1 ? 's' : ''} queued offline
          </p>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6 sm:py-8">
        {/* Daily Summary Widget */}
        <div className="card mb-6">
          <h2 className="text-lg sm:text-xl font-semibold mb-4 text-gray-800">Today's Summary</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-primary-50 rounded-lg">
              <p className="text-2xl sm:text-3xl font-bold text-primary-600">₹0</p>
              <p className="text-xs sm:text-sm text-gray-600 mt-1">Total Sales</p>
            </div>
            <div className="text-center p-3 bg-primary-50 rounded-lg">
              <p className="text-2xl sm:text-3xl font-bold text-primary-600">0</p>
              <p className="text-xs sm:text-sm text-gray-600 mt-1">Transactions</p>
            </div>
          </div>
        </div>

        {/* Large Microphone Button - 40% of screen height */}
        <div className="mb-6 flex justify-center">
          <button
            onClick={handleVoiceClick}
            className="relative flex flex-col items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 text-white rounded-full shadow-2xl transition-all duration-300 hover:scale-105 active:scale-95 touch-target"
            style={{ 
              width: 'min(280px, 70vw)', 
              height: 'min(280px, 40vh)',
              minWidth: '200px',
              minHeight: '200px'
            }}
            aria-label="Start voice recording"
          >
            <svg 
              className="w-20 h-20 sm:w-24 sm:h-24 mb-3" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
              />
            </svg>
            <span className="text-lg sm:text-xl font-bold">Record Transaction</span>
            <span className="text-xs sm:text-sm opacity-90 mt-1">Tap to speak</span>
            
            {/* Pulse animation ring */}
            <div className="absolute inset-0 rounded-full bg-primary-400 opacity-0 animate-ping" style={{ animationDuration: '2s' }}></div>
          </button>
        </div>

        {/* Quick Access Cards */}
        <div className="mt-8">
          <h2 className="text-lg sm:text-xl font-semibold mb-4 text-gray-800 px-1">Quick Access</h2>
          <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
            {/* Price Pulse */}
            <Link to="/prices" className="card hover:shadow-lg transition-all hover:scale-105 touch-target p-4">
              <div className="flex flex-col items-center text-center">
                <div className="w-12 h-12 sm:w-14 sm:h-14 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 sm:w-7 sm:h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-sm sm:text-base font-semibold mb-1">Price Pulse</h3>
                <p className="text-xs text-gray-600 hidden sm:block">Market prices</p>
              </div>
            </Link>

            {/* Freshness Scanner */}
            <Link to="/freshness" className="card hover:shadow-lg transition-all hover:scale-105 touch-target p-4">
              <div className="flex flex-col items-center text-center">
                <div className="w-12 h-12 sm:w-14 sm:h-14 bg-green-100 rounded-full flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 sm:w-7 sm:h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h3 className="text-sm sm:text-base font-semibold mb-1">Freshness</h3>
                <p className="text-xs text-gray-600 hidden sm:block">Scan produce</p>
              </div>
            </Link>

            {/* Marketplace */}
            <Link to="/marketplace" className="card hover:shadow-lg transition-all hover:scale-105 touch-target p-4">
              <div className="flex flex-col items-center text-center">
                <div className="w-12 h-12 sm:w-14 sm:h-14 bg-orange-100 rounded-full flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 sm:w-7 sm:h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-sm sm:text-base font-semibold mb-1">Marketplace</h3>
                <p className="text-xs text-gray-600 hidden sm:block">Sell B-Grade</p>
              </div>
            </Link>

            {/* Trust Score */}
            <Link to="/trust-score" className="card hover:shadow-lg transition-all hover:scale-105 touch-target p-4">
              <div className="flex flex-col items-center text-center">
                <div className="w-12 h-12 sm:w-14 sm:h-14 bg-purple-100 rounded-full flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 sm:w-7 sm:h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3 className="text-sm sm:text-base font-semibold mb-1">Trust Score</h3>
                <p className="text-xs text-gray-600 hidden sm:block">Your reputation</p>
              </div>
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Home
