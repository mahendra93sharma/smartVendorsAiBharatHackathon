import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface DemoModeContextType {
  isDemoMode: boolean
  toggleDemoMode: () => void
  showTutorial: boolean
  setShowTutorial: (show: boolean) => void
  offlineQueue: OfflineTransaction[]
  addToOfflineQueue: (transaction: OfflineTransaction) => void
  clearOfflineQueue: () => void
}

export interface OfflineTransaction {
  id: string
  type: 'voice' | 'marketplace' | 'price'
  data: Record<string, unknown>
  timestamp: number
}

const DemoModeContext = createContext<DemoModeContextType | undefined>(undefined)

const DEMO_MODE_KEY = 'smart-vendors-demo-mode'
const TUTORIAL_COMPLETED_KEY = 'smart-vendors-tutorial-completed'
const OFFLINE_QUEUE_KEY = 'smart-vendors-offline-queue'

export function DemoModeProvider({ children }: { children: ReactNode }) {
  const [isDemoMode, setIsDemoMode] = useState(() => {
    const saved = localStorage.getItem(DEMO_MODE_KEY)
    return saved === 'true'
  })

  const [showTutorial, setShowTutorial] = useState(() => {
    const completed = localStorage.getItem(TUTORIAL_COMPLETED_KEY)
    return completed !== 'true'
  })

  const [offlineQueue, setOfflineQueue] = useState<OfflineTransaction[]>(() => {
    const saved = localStorage.getItem(OFFLINE_QUEUE_KEY)
    return saved ? JSON.parse(saved) : []
  })

  useEffect(() => {
    localStorage.setItem(DEMO_MODE_KEY, isDemoMode.toString())
  }, [isDemoMode])

  useEffect(() => {
    localStorage.setItem(OFFLINE_QUEUE_KEY, JSON.stringify(offlineQueue))
  }, [offlineQueue])

  const toggleDemoMode = () => {
    setIsDemoMode((prev) => !prev)
  }

  const addToOfflineQueue = (transaction: OfflineTransaction) => {
    setOfflineQueue((prev) => [...prev, transaction])
  }

  const clearOfflineQueue = () => {
    setOfflineQueue([])
    localStorage.removeItem(OFFLINE_QUEUE_KEY)
  }

  const handleSetShowTutorial = (show: boolean) => {
    setShowTutorial(show)
    if (!show) {
      localStorage.setItem(TUTORIAL_COMPLETED_KEY, 'true')
    }
  }

  return (
    <DemoModeContext.Provider
      value={{
        isDemoMode,
        toggleDemoMode,
        showTutorial,
        setShowTutorial: handleSetShowTutorial,
        offlineQueue,
        addToOfflineQueue,
        clearOfflineQueue,
      }}
    >
      {children}
    </DemoModeContext.Provider>
  )
}

export function useDemoMode() {
  const context = useContext(DemoModeContext)
  if (context === undefined) {
    throw new Error('useDemoMode must be used within a DemoModeProvider')
  }
  return context
}
