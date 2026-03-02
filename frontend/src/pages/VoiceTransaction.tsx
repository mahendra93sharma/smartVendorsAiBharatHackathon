import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiService } from '../services/api'
import { DEMO_CREDENTIALS } from '../config/api'
import { useDemoMode } from '../contexts/DemoModeContext'
import { getRandomDemoAudio } from '../data/demoData'

interface TranscriptionResult {
  text: string
  confidence: number
  language: string
}

interface ExtractedTransaction {
  item_name: string
  quantity: number
  unit: string
  price_per_unit: number
  total_amount: number
  extracted_successfully: boolean
}

type RecordingState = 'idle' | 'recording' | 'processing' | 'completed' | 'error'

function VoiceTransaction() {
  const navigate = useNavigate()
  const { isDemoMode, addToOfflineQueue } = useDemoMode()
  const [recordingState, setRecordingState] = useState<RecordingState>('idle')
  const [transcription, setTranscription] = useState<TranscriptionResult | null>(null)
  const [transaction, setTransaction] = useState<ExtractedTransaction | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [recordingTime, setRecordingTime] = useState(0)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const timerRef = useRef<number | null>(null)

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current)
      }
    }
  }, [])

  const startRecording = async () => {
    try {
      setError(null)
      
      // Demo mode: use pre-recorded sample
      if (isDemoMode) {
        setRecordingState('recording')
        setRecordingTime(0)
        
        // Simulate recording for 2 seconds
        timerRef.current = window.setInterval(() => {
          setRecordingTime(prev => {
            if (prev >= 2) {
              if (timerRef.current) {
                window.clearInterval(timerRef.current)
              }
              processDemoAudio()
              return prev
            }
            return prev + 1
          })
        }, 1000)
        
        return
      }
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        await processAudio(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setRecordingState('recording')
      setRecordingTime(0)

      // Start timer
      timerRef.current = window.setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)

    } catch (err) {
      console.error('Error starting recording:', err)
      setError('Failed to access microphone. Please grant permission.')
      setRecordingState('error')
    }
  }

  const processDemoAudio = () => {
    setRecordingState('processing')
    
    // Simulate processing delay
    setTimeout(() => {
      const demoSample = getRandomDemoAudio()
      setTranscription(demoSample.transcription)
      setTransaction({
        ...demoSample.transaction,
        extracted_successfully: true,
      })
      setRecordingState('completed')
    }, 1500)
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && recordingState === 'recording') {
      mediaRecorderRef.current.stop()
      if (timerRef.current) {
        window.clearInterval(timerRef.current)
      }
      setRecordingState('processing')
    }
  }

  const processAudio = async (audioBlob: Blob) => {
    try {
      // Convert blob to base64
      const reader = new FileReader()
      reader.readAsDataURL(audioBlob)
      
      reader.onloadend = async () => {
        const base64Audio = reader.result as string
        const base64Data = base64Audio.split(',')[1]

        // Call voice transcription API
        const response = await apiService.post<{
          transcription: TranscriptionResult
          extracted_transaction: ExtractedTransaction
        }>('/voice/transcribe', {
          audio: base64Data,
          language_code: 'en-IN',
          vendor_id: DEMO_CREDENTIALS.vendorId,
          media_format: 'webm'
        })

        setTranscription(response.transcription)
        setTransaction(response.extracted_transaction)
        setRecordingState('completed')
      }

      reader.onerror = () => {
        throw new Error('Failed to read audio file')
      }

    } catch (err) {
      console.error('Error processing audio:', err)
      setError('Failed to process audio. Please try again.')
      setRecordingState('error')
    }
  }

  const handleConfirm = () => {
    // Check if offline - queue transaction
    if (!navigator.onLine && transaction) {
      addToOfflineQueue({
        id: `tx-${Date.now()}`,
        type: 'voice',
        data: transaction as unknown as Record<string, unknown>,
        timestamp: Date.now(),
      })
      navigate('/', { state: { message: 'Transaction queued offline. Will sync when online.' } })
      return
    }
    
    // Navigate back to home with success message
    navigate('/', { state: { message: 'Transaction recorded successfully!' } })
  }

  const handleReRecord = () => {
    setRecordingState('idle')
    setTranscription(null)
    setTransaction(null)
    setError(null)
    setRecordingTime(0)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getConfidenceLabel = (confidence: number) => {
    if (confidence >= 0.8) return 'High'
    if (confidence >= 0.6) return 'Medium'
    return 'Low'
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
            <h1 className="text-xl font-bold text-gray-900">Voice Transaction</h1>
          </div>
          {isDemoMode && (
            <span className="px-3 py-1 bg-primary-100 text-primary-700 text-sm font-medium rounded-full">
              Demo Mode
            </span>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Recording Interface */}
        {(recordingState === 'idle' || recordingState === 'recording') && (
          <div className="card text-center">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {recordingState === 'idle' ? 'Record Transaction' : 'Recording...'}
              </h2>
              <p className="text-gray-600">
                {recordingState === 'idle' 
                  ? 'Tap the microphone to start recording your transaction'
                  : 'Speak clearly about your transaction'}
              </p>
            </div>

            {/* Microphone Button with Waveform Animation */}
            <div className="flex justify-center mb-6">
              <button
                onClick={recordingState === 'idle' ? startRecording : stopRecording}
                className={`relative flex flex-col items-center justify-center rounded-full shadow-2xl transition-all duration-300 touch-target ${
                  recordingState === 'recording'
                    ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                    : 'bg-gradient-to-br from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 hover:scale-105'
                } text-white`}
                style={{ 
                  width: 'min(200px, 60vw)', 
                  height: 'min(200px, 60vw)',
                  minWidth: '150px',
                  minHeight: '150px'
                }}
                aria-label={recordingState === 'idle' ? 'Start recording' : 'Stop recording'}
              >
                <svg 
                  className="w-16 h-16 sm:w-20 sm:h-20" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  {recordingState === 'recording' ? (
                    <rect x="6" y="6" width="12" height="12" strokeWidth={2} />
                  ) : (
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
                    />
                  )}
                </svg>
                
                {recordingState === 'recording' && (
                  <>
                    {/* Waveform Animation Rings */}
                    <div className="absolute inset-0 rounded-full border-4 border-red-300 opacity-75 animate-ping" style={{ animationDuration: '1.5s' }}></div>
                    <div className="absolute inset-0 rounded-full border-4 border-red-400 opacity-50 animate-ping" style={{ animationDuration: '2s', animationDelay: '0.5s' }}></div>
                  </>
                )}
              </button>
            </div>

            {/* Recording Timer */}
            {recordingState === 'recording' && (
              <div className="mb-4">
                <p className="text-3xl font-bold text-red-600">{formatTime(recordingTime)}</p>
              </div>
            )}

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
              <h3 className="font-semibold text-blue-900 mb-2">Example phrases:</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• "Two kilos of tomatoes for fifty rupees"</li>
                <li>• "Sold three bunches of spinach at twenty rupees each"</li>
                <li>• "Five kilos potatoes, total one hundred rupees"</li>
              </ul>
            </div>
          </div>
        )}

        {/* Processing State */}
        {recordingState === 'processing' && (
          <div className="card text-center">
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mb-4"></div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Processing...</h2>
              <p className="text-gray-600">Transcribing and extracting transaction details</p>
            </div>
          </div>
        )}

        {/* Completed State - Show Results */}
        {recordingState === 'completed' && transcription && transaction && (
          <div className="space-y-6">
            {/* Transcription Result */}
            <div className="card">
              <div className="flex items-start justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-800">Transcription</h2>
                <div className="flex items-center">
                  <span className="text-sm text-gray-600 mr-2">Confidence:</span>
                  <span className={`text-sm font-semibold ${getConfidenceColor(transcription.confidence)}`}>
                    {getConfidenceLabel(transcription.confidence)} ({Math.round(transcription.confidence * 100)}%)
                  </span>
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-800 italic">"{transcription.text}"</p>
              </div>
            </div>

            {/* Extracted Transaction Details */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Transaction Details</h2>
              
              {transaction.extracted_successfully ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-primary-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-1">Item</p>
                      <p className="text-lg font-semibold text-gray-900">{transaction.item_name}</p>
                    </div>
                    <div className="bg-primary-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-1">Quantity</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {transaction.quantity} {transaction.unit}
                      </p>
                    </div>
                    <div className="bg-primary-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-1">Price per {transaction.unit}</p>
                      <p className="text-lg font-semibold text-gray-900">₹{transaction.price_per_unit.toFixed(2)}</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 border-2 border-green-200">
                      <p className="text-sm text-gray-600 mb-1">Total Amount</p>
                      <p className="text-2xl font-bold text-green-600">₹{transaction.total_amount.toFixed(2)}</p>
                    </div>
                  </div>

                  {/* Success Indicator */}
                  <div className="flex items-center justify-center text-green-600 mt-4">
                    <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="font-semibold">Transaction extracted successfully</span>
                  </div>
                </div>
              ) : (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex items-start">
                    <svg className="w-6 h-6 text-yellow-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <div>
                      <p className="font-semibold text-yellow-800 mb-1">Could not extract transaction details</p>
                      <p className="text-sm text-yellow-700">Please try recording again with clearer speech.</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleReRecord}
                className="flex-1 btn-secondary touch-target"
              >
                <div className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Re-record
                </div>
              </button>
              <button
                onClick={handleConfirm}
                className="flex-1 btn-primary touch-target"
                disabled={!transaction.extracted_successfully}
              >
                <div className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Confirm
                </div>
              </button>
            </div>
          </div>
        )}

        {/* Error State */}
        {recordingState === 'error' && error && (
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
                onClick={handleReRecord}
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

export default VoiceTransaction
