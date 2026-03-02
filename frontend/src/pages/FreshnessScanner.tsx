import { useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiService } from '../services/api'

interface ClassificationResult {
  category: 'Fresh' | 'B-Grade' | 'Waste'
  confidence: number
  shelf_life_hours?: number
  suggestions?: string[]
}

type ScanState = 'idle' | 'capturing' | 'processing' | 'completed' | 'error'

function FreshnessScanner() {
  const navigate = useNavigate()
  const [scanState, setScanState] = useState<ScanState>('idle')
  const [capturedImage, setCapturedImage] = useState<string | null>(null)
  const [classification, setClassification] = useState<ClassificationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  
  const fileInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const streamRef = useRef<MediaStream | null>(null)

  const startCamera = async () => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      })
      
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        videoRef.current.play()
      }
      setScanState('capturing')
    } catch (err) {
      console.error('Error accessing camera:', err)
      setError('Failed to access camera. Please grant permission or upload an image.')
      setScanState('error')
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
  }

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current
      const canvas = canvasRef.current
      
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.drawImage(video, 0, 0)
        const imageData = canvas.toDataURL('image/jpeg', 0.8)
        setCapturedImage(imageData)
        stopCamera()
        processImage(imageData)
      }
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setError(null)
      const reader = new FileReader()
      reader.onloadend = () => {
        const imageData = reader.result as string
        setCapturedImage(imageData)
        processImage(imageData)
      }
      reader.onerror = () => {
        setError('Failed to read image file')
        setScanState('error')
      }
      reader.readAsDataURL(file)
    }
  }

  const processImage = async (imageData: string) => {
    setScanState('processing')
    setUploadProgress(0)
    
    try {
      // Convert base64 to blob
      const base64Data = imageData.split(',')[1]
      const byteCharacters = atob(base64Data)
      const byteNumbers = new Array(byteCharacters.length)
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      const blob = new Blob([byteArray], { type: 'image/jpeg' })
      const file = new File([blob], 'produce.jpg', { type: 'image/jpeg' })

      // Upload and classify
      const response = await apiService.uploadFile<ClassificationResult>(
        '/freshness/classify',
        file,
        (progress) => setUploadProgress(progress)
      )

      setClassification(response)
      setScanState('completed')
    } catch (err) {
      console.error('Error processing image:', err)
      setError('Failed to classify image. Please try again.')
      setScanState('error')
    }
  }

  const handleRetake = () => {
    setScanState('idle')
    setCapturedImage(null)
    setClassification(null)
    setError(null)
    setUploadProgress(0)
  }

  const handleListOnMarketplace = () => {
    if (classification) {
      navigate('/marketplace', { 
        state: { 
          fromFreshness: true,
          category: classification.category 
        } 
      })
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Fresh': return 'bg-green-100 text-green-800 border-green-300'
      case 'B-Grade': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'Waste': return 'bg-red-100 text-red-800 border-red-300'
      default: return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Fresh':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )
      case 'B-Grade':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        )
      case 'Waste':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        )
      default:
        return null
    }
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
          <h1 className="text-xl font-bold text-gray-900">Freshness Scanner</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Idle State - Choose Input Method */}
        {scanState === 'idle' && (
          <div className="card text-center">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Scan Produce Freshness</h2>
              <p className="text-gray-600">
                Take a photo or upload an image to assess freshness
              </p>
            </div>

            {/* Camera Icon */}
            <div className="flex justify-center mb-6">
              <div className="w-32 h-32 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center">
                <svg className="w-16 h-16 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-4">
              <button
                onClick={startCamera}
                className="btn-primary w-full touch-target"
              >
                <div className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  </svg>
                  Open Camera
                </div>
              </button>

              <button
                onClick={() => fileInputRef.current?.click()}
                className="btn-secondary w-full touch-target"
              >
                <div className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Upload Image
                </div>
              </button>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              className="hidden"
            />

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left mt-6">
              <h3 className="font-semibold text-blue-900 mb-2">Tips for best results:</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Ensure good lighting</li>
                <li>• Center the produce in frame</li>
                <li>• Avoid shadows and reflections</li>
                <li>• Take photo from above or at eye level</li>
              </ul>
            </div>
          </div>
        )}

        {/* Capturing State - Camera View */}
        {scanState === 'capturing' && (
          <div className="card">
            <div className="relative">
              {/* Video Preview with Circular Overlay */}
              <div className="relative bg-black rounded-lg overflow-hidden" style={{ aspectRatio: '4/3' }}>
                <video
                  ref={videoRef}
                  className="w-full h-full object-cover"
                  autoPlay
                  playsInline
                />
                
                {/* Circular Overlay Guide */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="relative" style={{ width: '70%', aspectRatio: '1' }}>
                    <div className="absolute inset-0 rounded-full border-4 border-white opacity-50"></div>
                    <div className="absolute inset-0 rounded-full border-2 border-dashed border-white animate-pulse"></div>
                  </div>
                </div>

                {/* Instruction Overlay */}
                <div className="absolute top-4 left-0 right-0 text-center">
                  <div className="inline-block bg-black bg-opacity-60 text-white px-4 py-2 rounded-full text-sm">
                    Position produce in the circle
                  </div>
                </div>
              </div>

              {/* Capture Button */}
              <div className="flex justify-center mt-6 gap-4">
                <button
                  onClick={() => {
                    stopCamera()
                    setScanState('idle')
                  }}
                  className="btn-secondary touch-target"
                >
                  Cancel
                </button>
                <button
                  onClick={captureImage}
                  className="btn-primary touch-target flex-1"
                >
                  <div className="flex items-center justify-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    </svg>
                    Capture Photo
                  </div>
                </button>
              </div>
            </div>

            {/* Hidden canvas for image capture */}
            <canvas ref={canvasRef} className="hidden" />
          </div>
        )}

        {/* Processing State */}
        {scanState === 'processing' && (
          <div className="card text-center">
            {capturedImage && (
              <div className="mb-6">
                <img 
                  src={capturedImage} 
                  alt="Captured produce" 
                  className="w-full max-w-md mx-auto rounded-lg shadow-md"
                />
              </div>
            )}
            
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-green-600 mb-4"></div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Analyzing...</h2>
              <p className="text-gray-600 mb-4">Classifying produce freshness</p>
              
              {/* Upload Progress */}
              {uploadProgress > 0 && (
                <div className="w-full max-w-xs">
                  <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-green-600 h-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{uploadProgress}% uploaded</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Completed State - Show Classification Result */}
        {scanState === 'completed' && classification && capturedImage && (
          <div className="space-y-6">
            {/* Captured Image */}
            <div className="card">
              <img 
                src={capturedImage} 
                alt="Captured produce" 
                className="w-full rounded-lg shadow-md"
              />
            </div>

            {/* Classification Result */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Classification Result</h2>
              
              {/* Category Badge */}
              <div className="flex items-center justify-center mb-6">
                <div className={`flex items-center gap-3 px-6 py-4 rounded-xl border-2 ${getCategoryColor(classification.category)}`}>
                  {getCategoryIcon(classification.category)}
                  <div>
                    <p className="text-2xl font-bold">{classification.category}</p>
                    <p className="text-sm opacity-75">
                      Confidence: {Math.round(classification.confidence * 100)}%
                    </p>
                  </div>
                </div>
              </div>

              {/* Shelf Life (for Fresh category) */}
              {classification.category === 'Fresh' && classification.shelf_life_hours && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <div className="flex items-start">
                    <svg className="w-6 h-6 text-green-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                      <p className="font-semibold text-green-800 mb-1">Estimated Shelf Life</p>
                      <p className="text-green-700">
                        {classification.shelf_life_hours} hours ({Math.round(classification.shelf_life_hours / 24)} days)
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Suggestions */}
              {classification.suggestions && classification.suggestions.length > 0 && (
                <div className={`border rounded-lg p-4 ${
                  classification.category === 'B-Grade' 
                    ? 'bg-yellow-50 border-yellow-200' 
                    : 'bg-red-50 border-red-200'
                }`}>
                  <div className="flex items-start">
                    <svg className={`w-6 h-6 mr-2 flex-shrink-0 ${
                      classification.category === 'B-Grade' ? 'text-yellow-600' : 'text-red-600'
                    }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <div className="flex-1">
                      <p className={`font-semibold mb-2 ${
                        classification.category === 'B-Grade' ? 'text-yellow-800' : 'text-red-800'
                      }`}>
                        Suggestions
                      </p>
                      <ul className={`space-y-1 text-sm ${
                        classification.category === 'B-Grade' ? 'text-yellow-700' : 'text-red-700'
                      }`}>
                        {classification.suggestions.map((suggestion, index) => (
                          <li key={index}>• {suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="space-y-4">
              {classification.category === 'B-Grade' && (
                <button
                  onClick={handleListOnMarketplace}
                  className="btn-primary w-full touch-target"
                >
                  <div className="flex items-center justify-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    List on Marketplace
                  </div>
                </button>
              )}
              
              <button
                onClick={handleRetake}
                className="btn-secondary w-full touch-target"
              >
                <div className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Scan Another Item
                </div>
              </button>
            </div>
          </div>
        )}

        {/* Error State */}
        {scanState === 'error' && error && (
          <div className="card">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start">
                <svg className="w-6 h-6 text-red-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <p className="font-semibold text-red-800 mb-1">Error</p>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={handleRetake}
                className="btn-primary w-full touch-target"
              >
                Try Again
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default FreshnessScanner
