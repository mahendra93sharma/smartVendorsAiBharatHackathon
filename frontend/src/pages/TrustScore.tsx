import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { DEMO_CREDENTIALS } from '../config/api'

interface TrustScoreData {
  vendor_id: string
  trust_score: number
  tier: string
  next_tier: string | null
  next_threshold: number | null
  points_to_next_tier: number
}

interface ScoreBreakdown {
  transactions: number
  marketplace_sales: number
  consistency: number
}

function TrustScore() {
  const [trustScoreData, setTrustScoreData] = useState<TrustScoreData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showShareModal, setShowShareModal] = useState(false)

  useEffect(() => {
    loadTrustScore()
  }, [])

  const loadTrustScore = async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      const data = await apiService.get<TrustScoreData>(
        `/trust-score/${DEMO_CREDENTIALS.vendorId}`
      )
      setTrustScoreData(data)
    } catch (err) {
      console.error('Error loading trust score:', err)
      setError('Failed to load trust score')
      
      // Use mock data as fallback
      setTrustScoreData({
        vendor_id: DEMO_CREDENTIALS.vendorId,
        trust_score: 150,
        tier: 'Silver',
        next_tier: 'Gold',
        next_threshold: 250,
        points_to_next_tier: 100
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'Gold': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'Silver': return 'bg-gray-100 text-gray-800 border-gray-300'
      case 'Bronze': return 'bg-orange-100 text-orange-800 border-orange-300'
      default: return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getTierIcon = (tier: string) => {
    switch (tier) {
      case 'Gold':
        return (
          <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        )
      case 'Silver':
        return (
          <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        )
      case 'Bronze':
        return (
          <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        )
      default:
        return null
    }
  }

  const getProgressPercentage = () => {
    if (!trustScoreData || !trustScoreData.next_threshold) return 100
    
    const currentTierMin = trustScoreData.tier === 'Silver' ? 100 : 0
    const tierRange = trustScoreData.next_threshold - currentTierMin
    const progressInTier = trustScoreData.trust_score - currentTierMin
    
    return Math.min(100, Math.max(0, (progressInTier / tierRange) * 100))
  }

  const getScoreBreakdown = (): ScoreBreakdown => {
    if (!trustScoreData) return { transactions: 0, marketplace_sales: 0, consistency: 0 }
    
    // Mock breakdown based on total score
    // In a real app, this would come from the backend
    const transactions = Math.floor(trustScoreData.trust_score * 0.5)
    const marketplace_sales = Math.floor(trustScoreData.trust_score * 0.3)
    const consistency = Math.floor(trustScoreData.trust_score * 0.2)
    
    return { transactions, marketplace_sales, consistency }
  }

  const handleShareCertificate = () => {
    setShowShareModal(true)
    
    // Auto-close modal after 2 seconds
    setTimeout(() => {
      setShowShareModal(false)
    }, 2000)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Trust Score...</p>
        </div>
      </div>
    )
  }

  if (error && !trustScoreData) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center">
            <Link to="/" className="mr-4">
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <h1 className="text-xl font-bold text-gray-900">Trust Score</h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="card text-center">
            <svg className="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600 mb-4">{error}</p>
            <button onClick={loadTrustScore} className="btn-primary">
              Retry
            </button>
          </div>
        </main>
      </div>
    )
  }

  const breakdown = getScoreBreakdown()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center">
          <Link to="/" className="mr-4">
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <h1 className="text-xl font-bold text-gray-900">Trust Score</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6">
        {/* Tier Badge Card */}
        <div className="card text-center">
          <div className={`inline-flex items-center gap-3 px-6 py-4 rounded-xl border-2 ${getTierColor(trustScoreData?.tier || 'Bronze')}`}>
            {getTierIcon(trustScoreData?.tier || 'Bronze')}
            <div className="text-left">
              <p className="text-sm font-medium opacity-75">Current Tier</p>
              <p className="text-2xl font-bold">{trustScoreData?.tier}</p>
            </div>
          </div>
        </div>

        {/* Trust Score Progress Card */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-800">Trust Score</h2>
            <div className="text-right">
              <p className="text-3xl font-bold text-green-600">{trustScoreData?.trust_score}</p>
              {trustScoreData?.next_tier && (
                <p className="text-xs text-gray-600">
                  {trustScoreData.points_to_next_tier} points to {trustScoreData.next_tier}
                </p>
              )}
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mb-2">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>{trustScoreData?.tier}</span>
              {trustScoreData?.next_tier && (
                <span>{trustScoreData.next_tier}</span>
              )}
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className="bg-gradient-to-r from-green-500 to-green-600 h-4 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${getProgressPercentage()}%` }}
              ></div>
            </div>
            {trustScoreData?.next_threshold && (
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>{trustScoreData.tier === 'Silver' ? '100' : '0'}</span>
                <span>{trustScoreData.next_threshold}</span>
              </div>
            )}
          </div>

          {/* Next Tier Info */}
          {trustScoreData?.next_tier ? (
            <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-sm text-blue-800">
                <span className="font-semibold">Keep going!</span> Earn {trustScoreData.points_to_next_tier} more points to reach {trustScoreData.next_tier} tier
              </p>
            </div>
          ) : (
            <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <p className="text-sm text-yellow-800">
                <span className="font-semibold">Congratulations!</span> You've reached the highest tier
              </p>
            </div>
          )}
        </div>

        {/* Score Breakdown Card */}
        <div className="card">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Score Breakdown</h2>
          
          <div className="space-y-4">
            {/* Transactions */}
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-800">Transactions</p>
                  <p className="text-xs text-gray-600">+10 points per transaction</p>
                </div>
              </div>
              <p className="text-xl font-bold text-green-600">+{breakdown.transactions}</p>
            </div>

            {/* Marketplace Sales */}
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-800">Marketplace Sales</p>
                  <p className="text-xs text-gray-600">+20 points per sale</p>
                </div>
              </div>
              <p className="text-xl font-bold text-blue-600">+{breakdown.marketplace_sales}</p>
            </div>

            {/* Consistency */}
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                  <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-800">Consistency</p>
                  <p className="text-xs text-gray-600">+5 points per price report</p>
                </div>
              </div>
              <p className="text-xl font-bold text-purple-600">+{breakdown.consistency}</p>
            </div>
          </div>
        </div>

        {/* Share Certificate Button */}
        <button
          onClick={handleShareCertificate}
          className="btn-primary w-full touch-target flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
          Share Certificate
        </button>

        {/* How to Earn Points */}
        <div className="card bg-gradient-to-br from-green-50 to-blue-50 border border-green-200">
          <h3 className="text-lg font-bold text-gray-800 mb-3">How to Earn Points</h3>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex items-start gap-2">
              <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>+10 points</strong> for each voice transaction recorded</span>
            </li>
            <li className="flex items-start gap-2">
              <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>+20 points</strong> for each B-Grade marketplace sale</span>
            </li>
            <li className="flex items-start gap-2">
              <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>+5 points</strong> for each market price report</span>
            </li>
          </ul>
        </div>
      </main>

      {/* Share Modal */}
      {showShareModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 max-w-sm w-full animate-fade-in">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-gray-800 mb-2">Certificate Shared!</h3>
              <p className="text-sm text-gray-600">
                Your {trustScoreData?.tier} tier certificate has been shared successfully (Demo)
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TrustScore
