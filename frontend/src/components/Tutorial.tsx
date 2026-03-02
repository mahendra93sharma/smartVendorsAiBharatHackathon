import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

interface TutorialStep {
  title: string
  description: string
  route?: string
  highlight?: string
}

const TUTORIAL_STEPS: TutorialStep[] = [
  {
    title: 'Welcome to Smart Vendors!',
    description: 'This tutorial will guide you through the key features of the app. Tap anywhere to continue.',
  },
  {
    title: 'Voice Transactions',
    description: 'Record your sales by speaking in Hindi or English. Just tap the microphone and say "Do kilo tamatar, pachas rupaye".',
    route: '/voice',
    highlight: 'voice-button',
  },
  {
    title: 'Price Intelligence',
    description: 'Check market prices from nearby mandis before purchasing. Get the best deals and maximize your profit.',
    route: '/prices',
    highlight: 'price-card',
  },
  {
    title: 'Freshness Scanner',
    description: 'Scan your produce to check freshness. Get shelf life estimates and suggestions for B-Grade items.',
    route: '/freshness',
    highlight: 'freshness-card',
  },
  {
    title: 'Marketplace',
    description: 'Sell B-Grade produce to nearby buyers. Reduce waste and earn Mandi Credits for every sale.',
    route: '/marketplace',
    highlight: 'marketplace-card',
  },
  {
    title: 'Trust Score',
    description: 'Build your reputation and unlock financial services. Progress from Bronze to Silver to Gold tier.',
    route: '/trust-score',
    highlight: 'trust-card',
  },
  {
    title: "You're Ready!",
    description: 'Start using Smart Vendors to grow your business. You can replay this tutorial anytime from settings.',
  },
]

interface TutorialProps {
  onComplete: () => void
  onSkip: () => void
}

function Tutorial({ onComplete, onSkip }: TutorialProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const navigate = useNavigate()
  const step = TUTORIAL_STEPS[currentStep]

  useEffect(() => {
    // Navigate to the route if specified
    if (step.route) {
      navigate(step.route)
    }
  }, [currentStep, step.route, navigate])

  const handleNext = () => {
    if (currentStep < TUTORIAL_STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      onComplete()
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSkip = () => {
    navigate('/')
    onSkip()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75">
      {/* Tutorial Overlay */}
      <div className="relative max-w-md mx-4 bg-white rounded-lg shadow-2xl p-6">
        {/* Progress Indicator */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">
              Step {currentStep + 1} of {TUTORIAL_STEPS.length}
            </span>
            <button
              onClick={handleSkip}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Skip Tutorial
            </button>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / TUTORIAL_STEPS.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-3">{step.title}</h2>
          <p className="text-gray-600 leading-relaxed">{step.description}</p>
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              currentStep === 0
                ? 'text-gray-400 cursor-not-allowed'
                : 'text-primary-600 hover:bg-primary-50'
            }`}
          >
            Previous
          </button>
          <button
            onClick={handleNext}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            {currentStep === TUTORIAL_STEPS.length - 1 ? 'Get Started' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Tutorial
