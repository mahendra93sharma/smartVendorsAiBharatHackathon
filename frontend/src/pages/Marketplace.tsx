import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { apiService } from '../services/api'
import { DEMO_CREDENTIALS } from '../config/api'

interface MarketplaceListing {
  listing_id: string
  vendor_id: string
  item_name: string
  weight_kg: number
  condition: string
  price: number
  status: string
  created_at: string
  buyers_notified?: number
  mandi_credits_earned?: number
}

interface Buyer {
  buyer_id: string
  name: string
  type: string
  distance_km: number
  interested_items: string[]
}

interface CreateListingResponse {
  listing_id: string
  status: string
  buyers_notified: number
  mandi_credits_earned: number
}

interface VendorData {
  vendor_id: string
  trust_score: number
  tier: string
  mandi_credits: number
}

type ViewMode = 'create' | 'listings'

function Marketplace() {
  const location = useLocation()
  const [viewMode, setViewMode] = useState<ViewMode>('create')
  
  // Form state
  const [itemName, setItemName] = useState('')
  const [weight, setWeight] = useState('')
  const [price, setPrice] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [submitSuccess, setSubmitSuccess] = useState(false)
  
  // Listings state
  const [listings, setListings] = useState<MarketplaceListing[]>([])
  const [isLoadingListings, setIsLoadingListings] = useState(false)
  
  // Buyers state
  const [nearbyBuyers, setNearbyBuyers] = useState<Buyer[]>([])
  const [isLoadingBuyers, setIsLoadingBuyers] = useState(false)
  
  // Vendor state
  const [vendorData, setVendorData] = useState<VendorData>({
    vendor_id: DEMO_CREDENTIALS.vendorId,
    trust_score: 150,
    tier: 'Silver',
    mandi_credits: 450
  })

  // Check if coming from freshness scanner
  useEffect(() => {
    if (location.state?.fromFreshness && location.state?.category === 'B-Grade') {
      setViewMode('create')
    }
  }, [location.state])

  // Load vendor listings
  useEffect(() => {
    if (viewMode === 'listings') {
      loadVendorListings()
    }
  }, [viewMode])

  // Load nearby buyers when creating listing
  useEffect(() => {
    if (viewMode === 'create' && itemName) {
      loadNearbyBuyers(itemName)
    }
  }, [viewMode, itemName])

  const loadVendorListings = async () => {
    setIsLoadingListings(true)
    try {
      // In a real app, this would fetch from the backend
      // For demo, we'll use mock data
      const mockListings: MarketplaceListing[] = [
        {
          listing_id: 'listing-001',
          vendor_id: DEMO_CREDENTIALS.vendorId,
          item_name: 'Tomatoes',
          weight_kg: 5.0,
          condition: 'B-Grade',
          price: 150,
          status: 'active',
          created_at: new Date().toISOString(),
          buyers_notified: 5,
          mandi_credits_earned: 50
        },
        {
          listing_id: 'listing-002',
          vendor_id: DEMO_CREDENTIALS.vendorId,
          item_name: 'Potatoes',
          weight_kg: 10.0,
          condition: 'B-Grade',
          price: 200,
          status: 'sold',
          created_at: new Date(Date.now() - 86400000).toISOString(),
          buyers_notified: 3,
          mandi_credits_earned: 100
        }
      ]
      setListings(mockListings)
    } catch (error) {
      console.error('Error loading listings:', error)
    } finally {
      setIsLoadingListings(false)
    }
  }

  const loadNearbyBuyers = async (item: string) => {
    setIsLoadingBuyers(true)
    try {
      const buyers = await apiService.get<Buyer[]>('/marketplace/buyers', {
        item_name: item,
        radius_km: 10
      })
      setNearbyBuyers(buyers)
    } catch (error) {
      console.error('Error loading buyers:', error)
      // Use mock data as fallback
      setNearbyBuyers([
        {
          buyer_id: 'buyer-001',
          name: 'Delhi Juice Corner',
          type: 'juice_shop',
          distance_km: 2.5,
          interested_items: ['tomatoes', 'fruits']
        },
        {
          buyer_id: 'buyer-002',
          name: 'Pickle Factory',
          type: 'processing_unit',
          distance_km: 5.0,
          interested_items: ['tomatoes', 'onions']
        }
      ])
    } finally {
      setIsLoadingBuyers(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitError(null)
    setSubmitSuccess(false)

    // Validation
    if (!itemName.trim()) {
      setSubmitError('Please enter item name')
      return
    }
    if (!weight || parseFloat(weight) <= 0) {
      setSubmitError('Please enter valid weight')
      return
    }
    if (!price || parseFloat(price) <= 0) {
      setSubmitError('Please enter valid price')
      return
    }

    setIsSubmitting(true)

    try {
      const response = await apiService.post<CreateListingResponse>('/marketplace/listings', {
        vendor_id: vendorData.vendor_id,
        item_name: itemName,
        weight_kg: parseFloat(weight),
        price: parseFloat(price)
      })

      // Update Mandi Credits
      const creditsEarned = response.mandi_credits_earned || 0
      setVendorData(prev => ({
        ...prev,
        mandi_credits: prev.mandi_credits + creditsEarned
      }))

      setSubmitSuccess(true)
      
      // Reset form
      setTimeout(() => {
        setItemName('')
        setWeight('')
        setPrice('')
        setSubmitSuccess(false)
      }, 2000)

    } catch (error) {
      console.error('Error creating listing:', error)
      setSubmitError('Failed to create listing. Please try again.')
    } finally {
      setIsSubmitting(false)
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
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        )
      default:
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        )
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'sold': return 'bg-blue-100 text-blue-800'
      case 'expired': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="mr-4">
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <h1 className="text-xl font-bold text-gray-900">B-Grade Marketplace</h1>
          </div>
          
          {/* Mandi Credits Badge */}
          <div className={`flex items-center gap-2 px-3 py-2 rounded-lg border ${getTierColor(vendorData.tier)}`}>
            {getTierIcon(vendorData.tier)}
            <div className="text-right">
              <p className="text-xs font-medium opacity-75">{vendorData.tier}</p>
              <p className="text-sm font-bold">{vendorData.mandi_credits} Credits</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* View Mode Toggle */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setViewMode('create')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              viewMode === 'create'
                ? 'bg-green-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Create Listing
          </button>
          <button
            onClick={() => setViewMode('listings')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              viewMode === 'listings'
                ? 'bg-green-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            My Listings
          </button>
        </div>

        {/* Create Listing View */}
        {viewMode === 'create' && (
          <div className="space-y-6">
            {/* Listing Form */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Create New Listing</h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Item Name */}
                <div>
                  <label htmlFor="itemName" className="block text-sm font-medium text-gray-700 mb-2">
                    Item Name
                  </label>
                  <input
                    id="itemName"
                    type="text"
                    value={itemName}
                    onChange={(e) => setItemName(e.target.value)}
                    placeholder="e.g., Tomatoes, Potatoes"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                {/* Weight */}
                <div>
                  <label htmlFor="weight" className="block text-sm font-medium text-gray-700 mb-2">
                    Weight (kg)
                  </label>
                  <input
                    id="weight"
                    type="number"
                    step="0.1"
                    min="0"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    placeholder="e.g., 5.0"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                {/* Price */}
                <div>
                  <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-2">
                    Price (₹)
                  </label>
                  <input
                    id="price"
                    type="number"
                    step="1"
                    min="0"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    placeholder="e.g., 150"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                {/* Credits Info */}
                {weight && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-green-600 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                      </svg>
                      <div>
                        <p className="text-sm font-semibold text-green-800">
                          You'll earn {Math.round(parseFloat(weight) * 10)} Mandi Credits
                        </p>
                        <p className="text-xs text-green-700 mt-1">
                          10 credits per kg of B-Grade produce sold
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Error Message */}
                {submitError && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-red-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p className="text-sm text-red-700">{submitError}</p>
                    </div>
                  </div>
                )}

                {/* Success Message */}
                {submitSuccess && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-green-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p className="text-sm text-green-700 font-medium">Listing created successfully!</p>
                    </div>
                  </div>
                )}

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary w-full touch-target"
                >
                  {isSubmitting ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Creating Listing...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                      Create Listing
                    </div>
                  )}
                </button>
              </form>
            </div>

            {/* Nearby Buyers */}
            {itemName && (
              <div className="card">
                <h3 className="text-lg font-bold text-gray-800 mb-4">
                  Nearby Buyers
                  {!isLoadingBuyers && nearbyBuyers.length > 0 && (
                    <span className="ml-2 text-sm font-normal text-gray-600">
                      ({nearbyBuyers.length} interested)
                    </span>
                  )}
                </h3>

                {isLoadingBuyers ? (
                  <div className="flex justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
                  </div>
                ) : nearbyBuyers.length > 0 ? (
                  <div className="space-y-3">
                    {nearbyBuyers.map((buyer) => (
                      <div
                        key={buyer.buyer_id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
                      >
                        <div className="flex-1">
                          <p className="font-medium text-gray-800">{buyer.name}</p>
                          <p className="text-sm text-gray-600 capitalize">
                            {buyer.type.replace('_', ' ')}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-gray-800">
                            {buyer.distance_km} km
                          </p>
                          <p className="text-xs text-gray-600">away</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-600 text-center py-4">
                    Enter an item name to see nearby buyers
                  </p>
                )}

                {nearbyBuyers.length > 0 && (
                  <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p className="text-sm text-blue-800">
                      <span className="font-semibold">Auto-notification:</span> These buyers will be notified when you create your listing
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* My Listings View */}
        {viewMode === 'listings' && (
          <div className="card">
            <h2 className="text-xl font-bold text-gray-800 mb-4">My Active Listings</h2>

            {isLoadingListings ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
              </div>
            ) : listings.length > 0 ? (
              <div className="space-y-4">
                {listings.map((listing) => (
                  <div
                    key={listing.listing_id}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-bold text-gray-800">{listing.item_name}</h3>
                        <p className="text-sm text-gray-600">{listing.weight_kg} kg • ₹{listing.price}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(listing.status)}`}>
                        {listing.status}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-3 border-t border-gray-200">
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Buyers Notified</p>
                        <p className="text-lg font-bold text-gray-800">{listing.buyers_notified || 0}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Credits Earned</p>
                        <p className="text-lg font-bold text-green-600">{listing.mandi_credits_earned || 0}</p>
                      </div>
                    </div>

                    <p className="text-xs text-gray-500 mt-3">
                      Listed {new Date(listing.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <p className="text-gray-600 mb-2">No listings yet</p>
                <button
                  onClick={() => setViewMode('create')}
                  className="text-green-600 font-medium hover:text-green-700"
                >
                  Create your first listing
                </button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default Marketplace
