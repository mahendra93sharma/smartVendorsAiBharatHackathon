import { useState } from 'react'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'

interface PriceData {
  item_name: string
  mandi_name: string
  price_per_kg: number
  distance_km: number
  timestamp: string
}

interface PriceResponse {
  item: string
  prices: PriceData[]
  count: number
}

function PriceIntelligence() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [priceData, setPriceData] = useState<PriceResponse | null>(null)
  const [isListening, setIsListening] = useState(false)

  const handleVoiceInput = () => {
    // Check if browser supports Web Speech API
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Voice input not supported in this browser')
      return
    }

    const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognitionClass) {
      setError('Speech recognition not supported')
      return
    }
    const recognition = new SpeechRecognitionClass()

    recognition.lang = 'en-IN'
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onstart = () => {
      setIsListening(true)
      setError(null)
    }

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript
      setQuery(transcript)
      setIsListening(false)
    }

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      setError(`Voice input error: ${event.error}`)
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognition.start()
  }

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter an item name')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await apiService.get<PriceResponse>(`/prices/${encodeURIComponent(query.trim())}`)
      setPriceData(response)
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } }
      setError(error.response?.data?.error || 'Failed to fetch prices. Please try again.')
      setPriceData(null)
    } finally {
      setLoading(false)
    }
  }

  const getPriceColor = (price: number, prices: PriceData[]): string => {
    if (prices.length === 0) return 'text-gray-700'
    
    const priceValues = prices.map(p => p.price_per_kg)
    const minPrice = Math.min(...priceValues)
    const maxPrice = Math.max(...priceValues)
    const range = maxPrice - minPrice

    if (range === 0) return 'text-yellow-600'

    const threshold = range / 3
    if (price <= minPrice + threshold) return 'text-green-600'
    if (price >= maxPrice - threshold) return 'text-red-600'
    return 'text-yellow-600'
  }

  const getPriceBgColor = (price: number, prices: PriceData[]): string => {
    if (prices.length === 0) return 'bg-gray-50'
    
    const priceValues = prices.map(p => p.price_per_kg)
    const minPrice = Math.min(...priceValues)
    const maxPrice = Math.max(...priceValues)
    const range = maxPrice - minPrice

    if (range === 0) return 'bg-yellow-50'

    const threshold = range / 3
    if (price <= minPrice + threshold) return 'bg-green-50'
    if (price >= maxPrice - threshold) return 'bg-red-50'
    return 'bg-yellow-50'
  }

  const getPriceTrend = (price: number, prices: PriceData[]): string => {
    // Mock trend indicator - in production, this would compare with yesterday's price
    const priceValues = prices.map(p => p.price_per_kg)
    const avgPrice = priceValues.reduce((a, b) => a + b, 0) / priceValues.length
    
    if (price < avgPrice * 0.95) return '↓'
    if (price > avgPrice * 1.05) return '↑'
    return '→'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center">
          <Link to="/" className="mr-4">
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <h1 className="text-xl font-bold text-gray-900">Price Intelligence</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:py-8">
        {/* Query Interface */}
        <div className="card mb-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Check Market Prices</h2>
          
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex-1">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter item name (e.g., tomatoes, onions)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={loading || isListening}
              />
            </div>
            
            <button
              onClick={handleVoiceInput}
              disabled={loading || isListening}
              className={`px-6 py-3 rounded-lg font-semibold transition-all touch-target ${
                isListening
                  ? 'bg-red-500 text-white animate-pulse'
                  : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
              }`}
              aria-label="Voice input"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
            
            <button
              onClick={handleSearch}
              disabled={loading || isListening || !query.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed touch-target"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {isListening && (
            <p className="mt-3 text-sm text-blue-600 flex items-center">
              <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></span>
              Listening... Speak now
            </p>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Price Comparison Table */}
        {priceData && priceData.prices.length > 0 && (
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 text-gray-800">
              Prices for <span className="text-blue-600 capitalize">{priceData.item}</span>
            </h2>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-gray-200">
                    <th className="text-left py-3 px-2 text-sm font-semibold text-gray-700">Mandi</th>
                    <th className="text-right py-3 px-2 text-sm font-semibold text-gray-700">Price/kg</th>
                    <th className="text-right py-3 px-2 text-sm font-semibold text-gray-700">Distance</th>
                    <th className="text-center py-3 px-2 text-sm font-semibold text-gray-700">Trend</th>
                  </tr>
                </thead>
                <tbody>
                  {priceData.prices.map((price, index) => (
                    <tr 
                      key={index} 
                      className={`border-b border-gray-100 ${getPriceBgColor(price.price_per_kg, priceData.prices)}`}
                    >
                      <td className="py-4 px-2">
                        <div className="font-medium text-gray-900">{price.mandi_name}</div>
                      </td>
                      <td className="py-4 px-2 text-right">
                        <div className={`text-lg font-bold ${getPriceColor(price.price_per_kg, priceData.prices)}`}>
                          ₹{price.price_per_kg.toFixed(2)}
                        </div>
                      </td>
                      <td className="py-4 px-2 text-right">
                        <div className="text-sm text-gray-600">{price.distance_km.toFixed(1)} km</div>
                      </td>
                      <td className="py-4 px-2 text-center">
                        <span className="text-2xl">{getPriceTrend(price.price_per_kg, priceData.prices)}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Legend */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Price Indicators</h3>
              <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-green-50 border-2 border-green-600 rounded mr-2"></div>
                  <span className="text-gray-600">Low Price</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-yellow-50 border-2 border-yellow-600 rounded mr-2"></div>
                  <span className="text-gray-600">Medium Price</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-red-50 border-2 border-red-600 rounded mr-2"></div>
                  <span className="text-gray-600">High Price</span>
                </div>
                <div className="flex items-center ml-4">
                  <span className="text-xl mr-2">↑↓→</span>
                  <span className="text-gray-600">Price Trend</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* No Results */}
        {priceData && priceData.prices.length === 0 && (
          <div className="card text-center">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">No Prices Found</h3>
            <p className="text-gray-600">
              We couldn't find price data for "{priceData.item}". Try searching for common items like tomatoes, onions, or potatoes.
            </p>
          </div>
        )}

        {/* Initial State */}
        {!priceData && !loading && !error && (
          <div className="card text-center">
            <svg className="w-16 h-16 text-blue-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Check Market Prices</h3>
            <p className="text-gray-600 mb-4">
              Enter an item name or use voice input to check prices from nearby mandis
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              <button
                onClick={() => { setQuery('tomatoes'); }}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
              >
                Tomatoes
              </button>
              <button
                onClick={() => { setQuery('onions'); }}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
              >
                Onions
              </button>
              <button
                onClick={() => { setQuery('potatoes'); }}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
              >
                Potatoes
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default PriceIntelligence
